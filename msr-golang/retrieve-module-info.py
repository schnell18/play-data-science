#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import local functions
from datagrab.gomod import grab_gomod


def main(base_dir="mod-info", progress_file="progress.csv"):
    grab_gomod(
        "slim.csv",
        base_dir=base_dir,
        progress_file=progress_file,
        trace=True
    )

if __name__ == "__main__":
    main()
