#!/bin/bash

./identify-repos.py \
    --topic AI \
    --topic chatgpt \
    --topic OpenaI \
    --topic GenerativeAI \
    --output-dir ai-repos

./identify-repos.py \
    --lang golang \
    --topic AI \
    --topic chatgpt \
    --topic OpenaI \
    --topic GenerativeAI \
    --output-dir ai-repos

./identify-repos.py \
    --lang python \
    --lang c \
    --lang c++ \
    --topic AI \
    --topic chatgpt \
    --topic OpenaI \
    --topic GenerativeAI \
    --output-dir ai-repos

./identify-repos.py \
    --output-dir ai-repos
