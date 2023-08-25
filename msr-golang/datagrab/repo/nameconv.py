#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import requests

from html.parser import HTMLParser
from datetime import date, datetime, timedelta
from timeit import default_timer as timer
from pathlib import Path


class GoImportMetaHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._github_name = ""
       
    @property
    def github_name(self):
        return self._github_name
         
    def feed(self, text):
        self._gith_name = ""
        super().feed(text)

    def handle_starttag(self, tag, attrs):
        self._gith_name = ""
        if tag == "meta":
            imports_found = [attr for attr in attrs if attr[0] == "name" and attr[1] == "go-import"]
            contents = [attr[1] for attr in attrs if attr[0] == "content"]
            if imports_found and contents:
                comps = contents[0].split(' ')
                idx = comps[2].find("//")
                self._github_name = comps[2] if idx < 0 else comps[2][idx+2:]

def persist_progress(module, github_name, base_dir, progress_file):
    # persist mod info into files for later analysis
    mod_file = f"{base_dir}/{progress_file}"
    sub = Path(mod_file[0:-len(progress_file)])
    sub.mkdir(parents=True, exist_ok=True)
    if not Path(mod_file).exists():
        with open(mod_file, 'w') as f:
            f.write("module,github_name,last_updated\n")

    with open(mod_file, 'a') as f:
        f.write(f"{module},{github_name if github_name else '-'},{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


# client is the Github instance
# row is a row of Pandas DataFrame
def convert_name(parser, module, base_dir, progress_file, trace=False):
    t0 = timer()
    try:
        if trace: print(f"work on {module}")
        q = {"go-get": "1"}
        request_url = f"https://{module}"
        resp = requests.get(request_url, params=q, allow_redirects=True)
        parser.feed(resp.text)
        github_name = parser.github_name
        persist_progress(module, github_name, base_dir, progress_file)
        t1 = timer()
        if trace:
            print(f"Convert {module} to {github_name} took {t1-t0}s")
        return github_name
    except Exception as e:
        print(f"fail to convert {module} to github name due to {e}")

    return ""


def convert_names(repo_csv_file, base_dir="mod-info", progress_file="name-conv-progress.csv", trace=False):
    parser = GoImportMetaHTMLParser()
    to_check_df = pd.read_csv(repo_csv_file)

    progress_path = f"{base_dir}/{progress_file}"
    if Path(progress_path).exists():
        checked_df = pd.read_csv(progress_path)
        df2 = to_check_df.merge(checked_df, how="left", on="module")
        # filter already processed repos, equivalent to SQL is null
        df2 = df2.query("github_name != github_name")
        df2.apply(lambda r: convert_name(parser, r["module"], base_dir, progress_file, trace), axis=1)
    else:
        df2 = to_check_df
        df2.apply(lambda r: convert_name(parser, r["module"], base_dir, progress_file, trace), axis=1)
