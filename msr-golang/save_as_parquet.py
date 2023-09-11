#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import local functions
import parser.parquet as pp

if __name__ == "__main__":
    pp.snve_as_parquet(base_dir="tmp1/mod-info", dest_file="gomod2.parquet")

