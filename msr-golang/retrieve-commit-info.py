#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import local functions
from datagrab.github import grab_commits


def main(base_dir="commit-info", progress_file="progress.csv"):
    grab_commits(
        "go-awesome-repos.csv",
        base_dir=base_dir,
        progress_file=progress_file,
        trace=True
    )

if __name__ == "__main__":
    main()
