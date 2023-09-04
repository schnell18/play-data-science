#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
from datetime import date, timedelta

def load_access_token():
    parser = configparser.ConfigParser()
    parser.read('credential.ini')
    section = parser['github']
    return section['access_token']


def load_repo_info(client, repo_name):
    try:
        return client.get_repo(repo_name) 
    except Exception as e:
        print(f"Fail to locate {repo_name} due to: {e}")
        return None


def daterange(start_date, end_date, slice):
    tot_days = int((end_date - start_date).days) + 1
    periods = tot_days // slice
    remainder = tot_days % slice
    for n in range(periods):
        s = start_date + timedelta(n * slice)
        e = s + timedelta(slice - 1)
        yield (s, e)
    if remainder != 0:
        s = start_date + timedelta(periods * slice)
        e = s + timedelta(remainder - 1)
        yield (s, e)


def yearrange(start_year, end_year, slice):
    tot = end_year - start_year + 1
    periods = tot // slice
    remainder = tot % slice
    for n in range(periods):
        s = start_year + n * slice
        e = s + slice - 1
        yield (date(s, 1, 1), date(e, 12, 31))
    if remainder != 0:
        s = start_year + periods * slice
        e = s + remainder - 1
        yield (date(s, 1, 1), date(e, 12, 31))
        

def format_date(d):
    return d.strftime("%Y-%m-%d")
