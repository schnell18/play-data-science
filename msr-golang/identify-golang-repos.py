#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date, timedelta
from datagrab.github import collect_data


def main(base_dir="mod-info", progress_file="progress.csv"):

    subdir="go-repos"
    fork = True
    stars = 10
    slice = 15
    lang="golang"
    start_year = 2008
    end_year = 2022
    extra = (date(2023, 1, 1), date(2023, 9, 4))

    collect_data(start_year, end_year, extra, lang, fork, stars, slice, subdir, True)

if __name__ == "__main__":
    main()
