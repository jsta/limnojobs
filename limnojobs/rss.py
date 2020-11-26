import pandas as pd
import pkg_resources
import feedparser

from limnojobs.utils import filter_limno

# https://stackoverflow.com/questions/45701053/get-feeds-from-feedparser-and-import-to-pandas-dataframe

#### pull_feed fxn
def pull_feed(url, title):
    # url = rawrss['rawrss'][1]
    # title = rawrss['rawrss'][1]

    feed = feedparser.parse(url)

    subject_list = []
    body_list = []
    url_list = []
    for post in feed.entries:
        # post = feed.entries[0]
        subject_list.append(post.title)
        body_list.append(post.summary)
        url_list.append(post.link)

    res = pd.DataFrame({'subject': subject_list, 'body': body_list, 'url': url_list})

    return res

#### pull_rss fxn
def pull_rss():
    rawrss = pd.read_csv(pkg_resources.resource_filename('limnojobs',
                                                            'rss.csv'))
    # sort rawrss by increasing journal name nchar length for pretty printing
    rawrss.index = rawrss['title'].str.len()
    rawrss = rawrss.sort_index().reset_index(drop = True)

    # iterate here
    posts = pd.DataFrame(columns=['subject', 'body', 'url'])
    for i in range(len(rawrss.index)):
        # i = 0
        res_raw = pull_feed(rawrss['rawrss'][i], rawrss['title'][i])
        res = filter_limno(res_raw).reset_index()
        res['source'] = rawrss['title'][i]
        posts = posts.append(res, ignore_index=True)
    
    posts['subject'] = posts['subject'] + ' | ' + \
        posts['url'] + ' | ' + posts['source']

    return posts
