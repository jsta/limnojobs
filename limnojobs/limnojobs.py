import pandas as pd
import os
import sys
import inspect
from colorama import Fore
import twitter
import config

currentdir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from ecolog import pull_ecolog
from utils import filter_limno

# def limnojobs(tweet, interactive):
tweet = False
interactive = True

jobs_ecolog = pull_ecolog()
# jobs_rss = pull_rss()
# jobs_boards = pull_boards()

## TODO: append/concat data sources
jobs_all = jobs_ecolog

## test against log
log = pd.read_csv("../log.csv")
res = jobs_all[~jobs_all['subject'].isin(log['subject'])]# [['subject']]

## print/offer tweets
print(Fore.GREEN + "Filtered: ")
print()
jobs = res['subject'] + ". " + res['source'] + ". " + res['url']

for jobs in jobs:
    # job = jobs.iloc[0]
    print(Fore.GREEN + job)
    print()

if(tweet is True or interactive is True):
    api = twitter.Api(consumer_key=config.api_key,
                      consumer_secret=config.api_secret_key,
                      access_token_key = config.access_token_key,
                      access_token_secret=config.access_token_secret)
    # api.VerifyCredentials()

    jobs = jobs.sample(frac = 1)  # randomize jobs order
    # TODO: iterate through the 'index' of jobs rather than jobs themselves
    #           this is to produce the log of both subject and body below

    for job in jobs:
        # job = jobs.iloc[0]
        print(job)
        if(interactive is True):
            post_job = input("post limnojob (y)/n/i? ") or "y"
            if(post_job in ["y"]):
                status = api.PostUpdate(job)
                posted = "y"
            if(post_job in ["i"]):
                posted = "i"

                    if(post_subject in ["y", "i"]):
                        # write to log
                        log = pd.read_csv("../log.csv")
                        keys = ["source", "date", "flag", "subject",
                                "body"]

                        # subject = "title? journal. url"
                        # subject = "Annual 30-meter Dataset for  Glacial Lakes in High Mountain  Asia from 2008 to 2017. Earth System Science Data. https://doi.org/10.5194/essd-2020-57"
                        # posted = "y"
                        source = job['source']
                        date = str(datetime.date.today())
                        subject = job['subject']
                        body = job['body']
                        d = dict(zip(keys, [source, date, posted,
                                            subject, body]))

                        d = pd.DataFrame.from_records(d, index=[0])
                        log = log.append(pd.DataFrame(data = d),
                                         ignore_index = True)
                        log.to_csv("log.csv", index = False)
                else:
                    status = api.PostUpdate(toot)

                    # write to log
                    log = pd.read_csv("log.csv")
                    keys = ["title", "dc_source", "prism_url"]
                    title, dc_source, prism_url = toot_split(toot)
                    d = dict(zip(keys, [title, dc_source, prism_url]))
                    d = pd.DataFrame.from_records(d, index=[0])
                    log = log.append(pd.DataFrame(data = d))
                    log.to_csv("log.csv", index = False)
                post_toot = "n"