# Introduction

This project explores github to mining golang repositories.

## github

Github has user-friendly official APIs and there is a Python SDK,
[PyGithub][3], to make API call easier. There is an offline dataset called
[GHTorrent][4], which synchronizes data from github events periodically. This
dataset is available in MySQL dump and MongoDB format. It could be used to
analyze general github statistics. Alternatively, you can use [gharchive][5].
Or build you own like [this][6].

### Python virtual env recommendation
It is recommended to create separate Python virtual enviroment for this
project. Suppose you use the plain Python 3.x:

    python3 -m venv ~/python-envs/social-mining --upgrade-deps
    source ~/python-envs/social-mining/bin/activate
    pip3 install -r requirements.txt


### dependencies

This project requires:

- numpy
- pandas
- matplotlib
- jupyterlab
- PyGithub

[3]: https://pypi.org/project/PyGithub/
[5]: https://www.gharchive.org/
[6]: https://levelup.gitconnected.com/how-to-mine-github-data-in-2022-e9c70b3f61d3
