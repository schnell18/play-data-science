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

def search_repo_iteratively(client, dict_list, lang, fork, stars, start, end):
    fork_str = "true" if fork else "false"
    # query_str = f"lang:{lang} stars:>={stars} fork:{fork_str} archived:false template:false created:{start}..{end}";
    query_str = f"lang:{lang} stars:>={stars} fork:{fork_str} created:{start}..{end}";
    repositories = client.search_repositories(query_str, sort="stars", order="desc")
    for repo in repositories:
        old_dict = vars(repo)
        dict_list.append({k:v for k,v in old_dict['_rawData'].items()})
        

def collect_data(start_year, end_year, extra_year_range, lang, fork, stars, slice, subdir, trace=False):
    sub = Path(subdir)
    sub.mkdir(exist_ok=True)
    client = Github(load_access_token(), per_page=100)
    date_ranges = []
    for t in yearrange(start_year, end_year, 2):
        date_ranges.append(t)
    if (extra_year_range != None):
        date_ranges.append(extra_year_range)
        
    date_ranges = date_ranges[::-1]
    for date_range in date_ranges:
        t0 = timer()
        dict_list = []
        for t in daterange(date_range[0], date_range[1], slice):
            search_repo_iteratively(client, dict_list, lang, fork, stars, format_date(t[0]), format_date(t[1]))
        t1 = timer()
        if trace:
            print(f"Collect {lang} data between {date_range[0]} and {date_range[1]} took {t1-t0} seconds")
        df = pd.DataFrame(dict_list)
        df.to_csv("%s/%s-repo-%d-%s-%s.csv" % (subdir, lang, stars, date_range[0], date_range[1]))
        t2 = timer()
        if trace:
            print(f"Save {lang} data between {date_range[0]} and {date_range[1]} took {t2-t1} seconds")
    
    t3 = timer()
    cost_dfs = []
    for date_range in date_ranges:
        df = pd.read_csv("%s/%s-repo-%d-%s-%s.csv" % (subdir, lang, stars, date_range[0], date_range[1]))
        cost_dfs.append(df)
    combined = pd.concat(cost_dfs)
    combined.to_csv("%s/%s-repo-%d-combined.csv" % (subdir, lang, stars))
    t4 = timer()

    if trace:
        print(f"Combine and save {lang} data took {t4-t3} seconds")
