import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import pandas as pd

import utils

def pull_csdms():
    csdms_baseurl = 'https://csdms.colorado.edu/wiki/Jobs'

    response = requests.get(csdms_baseurl)
    soup = BeautifulSoup(response.text, 'html.parser')
    individual_pages = soup.findAll('a')

    detect_csdms_url = lambda x: re.findall(r'(?<=\<a href="\/wiki\/Jobs:)(.*)(?=" title="Jobs)', x)
    csdms_urls = [detect_csdms_url(str(x)) for x in individual_pages]
    csdms_urls = [csdms_baseurl + ":" + x[0] for x in csdms_urls if x != []]

    subject_list = []
    body_list = []
    url_list = []

    # TODO: pull only the first several csmds_urls bc we can assume function is run regularly
    for url in csdms_urls:
        # url = csdms_urls[2]
        print(url)

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # subject
        msg_subject = soup.find_all('b')[0]
        detect_subject = lambda x: re.findall(r'(?<=\<b\>).*(?=<\/b>)', x)
        msg_subject = detect_subject(str(msg_subject))[0]
        
        # body
        msg_body = soup.find_all('p')
        if len(msg_body) == 0:
            msg_body = soup.find_all('div', class_ = 'col-sm-9')        
        
        # url
        msg_url = soup.find_all('a', class_ = 'external text')
        if len(msg_url) > 0:
            detect_url = lambda x: re.findall(r'(?<=target="_blank">).*(?=<\/a>)', x)
            msg_url = detect_url(str(msg_url))[0]
        else:
            msg_url = url                

        # --- #    
        subject_list.append(str(msg_subject))
        body_list.append(str(msg_body[0]))
        url_list.append(msg_url)
        
    res = pd.DataFrame({'subject': subject_list, 'body': body_list, 'url': url_list})
    res['source'] = '[CSDMS]'
    res['subject'] = res['subject'] + ' | ' + \
        res['url'] + ' | ' + res['source']

    if len(res) > 0:
        res = utils.filter_limno(res)

    return res


# nalms
