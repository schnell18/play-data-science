#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import local functions
from datagrab.repo import convert_names

if __name__ == "__main__":
    convert_names(
        "module-refs.csv",
        base_dir="mod-info.oci",
        trace=True
    )

