#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

import semver
# import json
# import requests
import configparser
import time
from github import Github
from datetime import date, datetime, timedelta
from timeit import default_timer as timer
from pathlib import Path


def load_access_token():
    parser = configparser.ConfigParser()
    parser.read('credential.ini')
    section = parser['github']
    return section['access_token']


# semver comparison
def semver_sort(ver_list):
    svers = [semver.version.Version.parse(v[1:] if v.startswith("v") else v) for v in ver_list]
    svers.sort(reverse=True)
    return [f"v{sv}" for sv in svers]


def load_gomod(repo, path, version):
    try:
        content = repo.get_contents(path, ref=version)
        return (True, content)
    except Exception as e:
        print(f"Fail to load {repo.full_name}/{path}@{version} due to: {e}")
        return (False, None)


def persist_gomod(owner, repo_name, version, content, gmod_path, base_dir="mod-info"):
    # persist mod info into files for later analysis
    mod_file = f"{base_dir}/{owner}/{repo_name}/{version}/{gmod_path}"
    sub = Path(mod_file[0:-len('go.mod')])
    sub.mkdir(parents=True, exist_ok=True)
    with open(mod_file, 'wb') as f:
        f.write(content)
        
def persist_progress(owner, repo_name, use_module, base_dir="mod-info", progress_file="progress.csv"):
    # persist mod info into files for later analysis
    mod_file = f"{base_dir}/{progress_file}"
    sub = Path(mod_file[0:-len(progress_file)])
    sub.mkdir(parents=True, exist_ok=True)
    if not Path(mod_file).exists():
        with open(mod_file, 'w') as f:
            f.write("full_name,use_module,last_updated\n")

    with open(mod_file, 'a') as f:
        f.write(f"{owner}/{repo_name},{1 if use_module else 0},{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


def format_date(d):
    return d.strftime("%Y-%m-%d")


def load_mod_info(client, owner, repo_name, base_dir="mod-info"):

    mod_count = 0
    repo = client.get_repo(f"{owner}/{repo_name}")
    # try all tagged versions plus latest version on default branch
    # content = repo.get_contents("go.mod", ref="v0.3.0")
    tags = repo.get_tags()
    vers = [t.name for t in tags if t.name.startswith('v') and semver.version.Version.is_valid(t.name[1:])]
    if len(vers) == 0:
        vers.append(repo.default_branch)
    else:
        # sort vers according to semver
        vers = semver_sort(vers)

    for ver in vers:
        ok, content = load_gomod(repo, "go.mod", ver)
        if ok:
            persist_gomod(owner, repo_name, ver, content.decoded_content, "go.mod", base_dir)
            mod_count += 1
        else:
            # search in sub directory, descend one level
            contents = repo.get_contents(".", ref=ver)
            subdirs = [c.name for c in contents if c.type == 'dir' and not c.name.startswith('.')]
            for subdir in subdirs:
                gmod_path = f"{subdir}/go.mod"
                ok, content = load_gomod(repo, gmod_path, ver)
                if ok:
                    persist_gomod(owner, repo_name, ver, content.decoded_content, gmod_path, base_dir)
                    mod_count += 1
                    break
            else: break

    return mod_count > 0

# client is the Github instance
# row is a row of Pandas DataFrame
def do_mod_check(client, row, base_dir="mod-info", progress_file="progress.csv", show_progress=False):
    comps = row['full_name'].split('/')
    owner = comps[0]
    name = comps[1]


    t0 = timer()
    use_module = load_mod_info(client, owner, name, base_dir)
    persist_progress(owner, name, use_module, base_dir, progress_file)
    t1 = timer()
    if show_progress:
        print(f"Grab gomod for {owner}/{name} took {t1-t0}s")
    return use_module


def grab_gomod(repo_csv_file, base_dir="mod-info", progress_file="progress.csv", show_progress=False):
    client = Github(load_access_token(), per_page=100) 
    to_check_df = pd.read_csv(repo_csv_file)

    progress_path = f"{base_dir}/{progress_file}"
    if Path(progress_path).exists():
        checked_df = pd.read_csv(progress_path)
        df2 = to_check_df.merge(checked_df, how="left", on="full_name")
        # filter already processed repos, equivalent to SQL is null
        df2 = df2.query("use_module != use_module")
        df2.apply(lambda r: do_mod_check(client, r, base_dir, progress_file, show_progress), axis=1)
    else:
        df2 = to_check_df
        df2.apply(lambda r: do_mod_check(client, r, base_dir, progress_file, show_progress), axis=1)