#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import local functions
from parser import parse_deps


if __name__ == "__main__":
    parse_deps(base_dir="mod-info.oci", trace=True)
