#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import local functions
from parser import parse_deps_from_parquet
from parser import parse_deps_from_dir
from timeit import default_timer as timer


if __name__ == "__main__":

    t0 = timer()
    parse_deps_from_parquet(parquet_file="gomod2.parquet", deps_file="dependencies-parquet2.csv", trace=True)
    t1 = timer()
    print(f"parse_deps_from_parquet() took {t1-t0}s")
    # parse_deps_from_dir(base_dir="tmp1/mod-info", deps_file="dependencies-dir.csv", trace=True)
    # t2 = timer()
    # print(f"parse_deps_from_dir() took {t2-t1}s")
