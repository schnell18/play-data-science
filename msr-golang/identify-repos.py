#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from datetime import date, datetime, timedelta
from datagrab.github import collect_data


def validate_date(date_string):
    try:
        # Attempt to parse the date string
        datetime.strptime(date_string, '%Y-%m-%d')
        return date_string
    except ValueError:
        raise argparse.ArgumentTypeError('Invalid date format. Please use YYYY-MM-DD.')


def parse_args():

    # Create the parser
    parser = argparse.ArgumentParser(description='Github repository finder')
    
    # Add arguments
    parser.add_argument('-o', '--output-dir', required=True, help='Path to save output files')
    parser.add_argument('-f', '--fork', action="store_true", default=False, help='Include forked repostory')
    parser.add_argument('-l', '--lang', help='Main language of the repository')
    parser.add_argument('-t', '--topic', action="append", help='Topic to search, repeat this option to specify multiple topics')
    parser.add_argument('-d', '--trace', action="store_true", default=False, help='Print trace messages')
    parser.add_argument('-s', '--stars', default=10, help='Minimal stars')
    parser.add_argument('--span', default=15, help='Days in one search trial, default 15')
    parser.add_argument('--start-year', type=int, default=2008, help='Start year of the search, in YYYY format, default 2008')
    parser.add_argument('--end-date', type=validate_date, default=datetime.today().strftime("%Y-%m-%d"), help='End date in YYYY-MM-DD format of the search, default today')
    
    # Parse the arguments
    args = parser.parse_args()
    if (args.lang is None or args.lang == '') and (args.topic is None or len(args.topic) == 0):
        parser.error("Either --topic or --lang is mandatory")
    return args


if __name__ == "__main__":
    args = parse_args()
    print(args)

    subdir     = args.output_dir
    fork       = args.fork
    trace      = args.trace
    stars      = args.stars
    slice      = args.span
    lang       = args.lang
    start_year = args.start_year
    topics     = args.topic
    end_date   = datetime.strptime(args.end_date, "%Y-%m-%d")
    end_year   = end_date.year - 1
    extra      = (date(end_date.year, 1, 1), end_date.date())

    collect_data(
        start_year, end_year, extra, fork, stars, slice, subdir,
        lang, topics=topics, trace=trace 
    )

