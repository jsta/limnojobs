import pandas as pd
import os
import sys
import inspect
from colorama import Fore
import twitter
import config
import datetime
import argparse

# execute from limnojobs/limnojobs
import listservs
import sheets
import rss
import boards

currentdir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

def limnotoots(tweet = False, interactive = False, unseen = True):
    r"""Filter limnology themed papers from a pandas DataFrame.
    :param tweet: boolean. Post tweets of limnojobs
    :param interactive: boolean. Ask for approval before tweeting.    
    :param unseen: boolean. Limit listserv queries to only unseen messages
    """

    def print_source(x):
        sys.stdout.write('\b' * 1000)
        sys.stdout.write('Fetching jobs from: ' + x + '\r')

    print_source("RSS")
    jobs_rss = rss.pull_rss()
    print_source("CSDMS")
    jobs_csdms = boards.pull_csdms()
    print_source("ECOLOG")
    jobs_ecolog = listservs.pull_ecolog(unseen = unseen)
    print_source("ECOEVO")
    jobs_ecoevo = sheets.pull_ecoevo()
    print_source("EarthEnvScience")
    jobs_earthenvscience = sheets.pull_earthenvscience()
    # jobs_boards = pull_boards()

    ## append/concat data sources
    jobs_all = pd.concat([jobs_ecolog, jobs_ecoevo, jobs_earthenvscience, jobs_rss, jobs_csdms])
    # jobs_all = jobs_ecolog

    ## test against log
    log = pd.read_csv("log.csv")
    res = jobs_all[~jobs_all['subject'].isin(log['subject'])]# [['subject']]
    res = res.sample(frac = 1)  # randomize jobs order

    ## print/offer tweets
    jobs = res['subject']
    print(Fore.GREEN + "Filtered: ")
    print()
    for job in jobs:
        # job = jobs.iloc[0]
        print(Fore.GREEN + job)
        print()

    if(tweet is True or interactive is True):
        api = twitter.Api(consumer_key=config.api_key,
                        consumer_secret=config.api_secret_key,
                        access_token_key = config.access_token_key,
                        access_token_secret=config.access_token_secret)
        # api.VerifyCredentials()

        for i in range(len(res)):
            # i = 0            
            job = jobs.iloc[i]
            print(job)
            if(interactive is True):
                post_job = input("post limnojob (y)/n/i? ") or "y"
                if(post_job in ["y"]):
                    status = api.PostUpdate(job)
                    posted = "y"
                if(post_job in ["i"]):
                    posted = "i"

                if(post_job in ["y", "i"]):
                    # write to log                
                    keys = ["source", "date", "flag", "subject", "body"]
                    source = res.iloc[i]['source']
                    date = str(datetime.date.today())
                    subject = res.iloc[i]['subject']
                    body = res.iloc[i]['body']                
                    d = dict(zip(keys, [source, date, posted,
                                        subject, body]))

                    d = pd.DataFrame.from_records(d, index=[0])
                    log = log.append(pd.DataFrame(data = d), ignore_index = True)
                    log.to_csv("log.csv", index = False)
            else:
                status = api.PostUpdate(toot)

                keys = ["source", "date", "flag", "subject", "body"]
                source = res.iloc[i]['source']
                date = str(datetime.date.today())
                subject = res.iloc[i]['subject']
                body = res.iloc[i]['body']                
                d = dict(zip(keys, [source, date, posted,
                                    subject, body]))

                d = pd.DataFrame.from_records(d, index=[0])
                log = log.append(pd.DataFrame(data = d), ignore_index = True)
                log.to_csv("log.csv", index = False)
            post_job = "n"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tweet', default = False,
                        action='store_true')
    parser.add_argument('--interactive', default = False,
                        action='store_true')
    parser.add_argument('--unseen', default = True,
                        action='store_false')
    args = parser.parse_args()

    limnotoots(tweet = args.tweet, interactive = args.interactive, unseen = args.unseen)


if __name__ == "__main__":
    main()
