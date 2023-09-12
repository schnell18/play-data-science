#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

# import local functions
from datagrab.github import grab_commits

def parse_args():

    # Create the parser
    parser = argparse.ArgumentParser(description='Github repository commit retriever')
    
    # Add arguments
    parser.add_argument('-o', '--output-dir', required=True, help='Path to save output files')
    parser.add_argument('-f', '--repo-list-file', required=True, help='The list of repository to retrieve commits')
    parser.add_argument('-d', '--trace', action="store_true", default=False, help='Print trace messages')
    parser.add_argument('--progress-file', default="progress.csv", help='File to save the commit retrieval progress, default progress.csv')
    
    # Parse the arguments
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    print(args)

    repo_list_file = args.repo_list_file
    progress_file  = args.progress_file
    subdir         = args.output_dir
    trace          = args.trace

    grab_commits(repo_list_file, base_dir=subdir, progress_file=progress_file, trace=trace)
