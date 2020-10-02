import pandas as pd
import os
import sys
import inspect
from colorama import Fore
import twitter

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

## append/concat data sources
res = jobs_ecolog

## test against log
log = pd.read_csv("../log.csv")
res = res[~res['subject'].isin(log['subject'])][['subject']]

## print/offer tweets
print(Fore.GREEN + "Filtered: ")
print()
subjects = res['subject'].copy()
subjects[subjects.str.len() > 159] = \
    subjects[subjects.str.len() > 159]. \
    str.slice(0, 159) + "..."
for subject in subjects:
    # print(Fore.GREEN + subject)
    print(subject)
    print()

if(tweet is True or interactive is True):
    api = twitter.Api(consumer_key=config.consumer_key,
                      consumer_secret=config.consumer_secret,
                      access_token_key = config.access_token_key,
                      access_token_secret=config.access_token_secret)

                      subjects = subjects.sample(frac = 1)  # randomize subjects order
            for subject in subjects:
                print(subject)
                if(interactive is True):
                    post_subject = input("post limnojob (y)/n/i? ") or "y"
                    if(post_subject in ["y"]):
                        status = api.PostUpdate(subject)
                        posted = "y"
                    if(post_subject in ["i"]):
                        posted = "i"

                    if(post_subject in ["y", "i"]):
                        # write to log
                        log = pd.read_csv("log.csv")
                        # keys = ["title", "dc_source", "prism_url", "posted",
                        #         "date"]

                        # subject = "title? journal. url"
                        # subject = "Annual 30-meter Dataset for  Glacial Lakes in High Mountain  Asia from 2008 to 2017. Earth System Science Data. https://doi.org/10.5194/essd-2020-57"
                        # posted = "y"                        
                        date = str(datetime.date.today())
                        d = dict(zip(keys, [title, dc_source, prism_url,
                                            posted, date]))
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