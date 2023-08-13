# Introduction

This project explores social data mining with twitter/google etc.

## google

Google trends has no official API. However, there is a community maintained
python library called [pytrends][1] can be used to do automated data collection
rather than using the [Google Trends][2] web page.


## github

Github has user-friendly official APIs and there is a Python SDK,
[PyGithub][3], to make API call easier. There is an offline dataset called
[GHTorrent][4], which synchronizes data from github events periodically. This
dataset is available in MySQL dump and MongoDB format. It could be used to
analyze general github statistics. Alternatively, you can use [gharchive][5].
Or build you own like [this][6].

## twitter

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
- twitter

### conclusion

Twitter closed the most free APIs access around March 2023.
Without a paid account, social mining is literally impossible.


[1]: https://pypi.org/project/pytrends/
[2]: https://trends.google.com/
[3]: https://pypi.org/project/PyGithub/
[4]: 
[5]: https://www.gharchive.org/
[6]: https://levelup.gitconnected.com/how-to-mine-github-data-in-2022-e9c70b3f61d3
