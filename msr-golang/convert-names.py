#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import local functions
from datagrab.repo import convert_names

if __name__ == "__main__":
    convert_names(
        "name-conv-module-refs.csv",
        progress_file="name-conv-progress.csv",
        trace=True
    )

