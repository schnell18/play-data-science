#!/usr/bin/env python
# -*- coding: utf-8 -*-

from github import Github
from datagrab.github import (
    load_access_token,
    load_latest_ver,
)

if __name__ == "__main__":

    client = Github(load_access_token(), per_page=100) 
    repos = [
        "pkg/errors",
        "spf13/pflag",
        "stretchr/testify",
        "go-yaml/yaml",
        "google/uuid",
        "gorilla/mux",
        "sirupsen/logrus",
        "mitchellh/go-homedir",
        "go-yaml/yaml",
        "davecgh/go-spew",
        "golang/protobuf",
        "golang/mock",
        "ghodss/yaml",
        "gorilla/websocket",
        "olekukonko/tablewriter",
        "blang/semver",
        "spf13/cobra",
        "fatih/color",
        "kubernetes-sigs/yaml",
        "hashicorp/go-multierror",
    ]
    for repo in repos:
        owner, repo_name = repo.split("/")
        latest_ver = load_latest_ver(client, owner, repo_name)
        print(f"{repo},{latest_ver}")

