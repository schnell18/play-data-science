#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import local functions
from datagrab.repo import convert_name
from datagrab.repo import GoImportMetaHTMLParser


if __name__ == "__main__":
    parser = GoImportMetaHTMLParser()
    # convert_name(parser, "go.openviz.dev/apimachinery", ".", "debug.csv", True)
    # convert_name(parser, "gopkg.in/elazarl/goproxy.v1", ".", "debug.csv", True)
    # convert_name(parser, "go.m3o.com", ".", "debug.csv", True)
    # convert_name(parser, "admiralty.io/multicluster-service-account", ".", "debug.csv", True)
    convert_name(parser, "k8s.io/client-go", ".", "debug.csv", True)


    # convert_name(parser, "xorm.io/builder", ".", "debug.csv", True)conv

