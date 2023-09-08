#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .common import daterange
from .common import format_date
from .common import load_access_token
from .common import yearrange
from github import Github
from pathlib import Path
from timeit import default_timer as timer
import configparser
import time
import numpy as np
import pandas as pd

def search_repo_iteratively(client, dict_list, fork, stars, start, end, langs=[], topics=[]):
    fork_str = "true" if fork else "false"
    query_str = f"stars:>={stars} fork:{fork_str} created:{start}..{end}";
    if langs is not None and len(langs) > 0:
        query_str += " "
        query_str += "+".join([f"lang:{lang}" for lang in langs])
    if topics is not None and len(topics) > 0:
        query_str += " "
        query_str += "+".join([f"topic:{topic}" for topic in topics])
    repositories = client.search_repositories(query_str, sort="stars", order="desc")
    for repo in repositories:
        old_dict = vars(repo)
        dict_list.append({k:v for k,v in old_dict['_rawData'].items()})
        

def collect_data(start_year, end_year, extra_year_range, fork, stars, slice, subdir, langs=[], topics=[], trace=False):
    sub = Path(subdir)
    sub.mkdir(exist_ok=True)
    client = Github(load_access_token(), per_page=100)
    date_ranges = []
    for t in yearrange(start_year, end_year, 2):
        date_ranges.append(t)
    if (extra_year_range != None):
        date_ranges.append(extra_year_range)
        
    date_ranges = date_ranges[::-1]
    search_key = _search_key(langs, topics)
    for date_range in date_ranges:
        t0 = timer()
        dict_list = []
        for t in daterange(date_range[0], date_range[1], slice):
            search_repo_iteratively(client, dict_list, fork, stars, format_date(t[0]), format_date(t[1]), langs=langs, topics=topics)
        t1 = timer()
        if trace:
            print(f"Collect {search_key} data between {date_range[0]} and {date_range[1]} took {t1-t0} seconds")
        df = pd.DataFrame(dict_list)
        df.to_csv("%s/%s-repo-%d-%s-%s.csv" % (subdir, search_key, stars, date_range[0], date_range[1]))
        t2 = timer()
        if trace:
            print(f"Save {search_key} data between {date_range[0]} and {date_range[1]} took {t2-t1} seconds")
    
    t3 = timer()
    cost_dfs = []
    for date_range in date_ranges:
        df = pd.read_csv("%s/%s-repo-%d-%s-%s.csv" % (subdir, search_key, stars, date_range[0], date_range[1]))
        cost_dfs.append(df)
    combined = pd.concat(cost_dfs)
    combined.to_csv("%s/%s-repo-%d-combined.csv" % (subdir, search_key, stars))
    t4 = timer()

    if trace:
        print(f"Combine and save {search_key} data took {t4-t3} seconds")

def _search_key(langs, topics):
    lng = ""
    tpc = ""
    if langs is not None: lng = "-".join(langs)
    if topics is not None: tpc = "-".join([x.replace(' ', '_') for x in t])

    if lng == "": return tpc
    if tpc == "": return lng
    return f"{lng}_{tpc}"
