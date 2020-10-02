# limnojobs

[![Build Status](https://api.travis-ci.org/jsta/limnojobs.png)](https://travis-ci.org/jsta/limnojobs) [![Feed Status](https://img.shields.io/badge/feed%20status-good-green.svg)](https://jsta.github.io/limnojobs)

Code to monitor [email listservs](limnojobs/listservs.csv), [RSS feeds](limnojobs/rss.csv), [Community job boards](limnojobs/boards.csv) and [tweet](https://twitter.com/limno_jobs) new jobs.

## Scope

The keywords and data streams herein aim to focus on limnology (the study of inland waters) and specifically on postdoc and assistant professor jobs in North America. 

## Usage

Query jobs that came out prior to today without tweeting:

`python limnojobs/limnojobs.py`

Manually approve tweeting of jobs that came out prior to today:

`python limnojobs/limnojobs.py --interactive`

Unsupervised tweeting of jobs that came out prior to today:

`python limnojobs/limnojobs.py --tweet`

## Setup

### Enable tweeting (optional)

* Create a file named `config.py` that stores your twitter API keys

### Enable unsupervised tweeting (optional)

* Create a _cron_ job. On Linux this can be done with the following commands:

```
crontab -e 
0 15 * * * python /path/to/limnojobs.py
```

### Python dependencies

See [requirements.txt](requirements.txt)

Install these to the activated environment with:

`pip install -r requirements.txt`

## Contributing

* Filtering keywords are located in [limnojobs/keywords.csv](limnojobs/keywords.csv).

## Prior art

https://github.com/jsta/limnopapers
