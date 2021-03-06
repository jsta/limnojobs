# https://www.geeksforgeeks.org/python-fetch-your-gmail-emails-from-a-particular-user/

import email
import imaplib
import re
import pandas as pd
import pkg_resources
import datetime
import numpy as np

import utils

try:
    import config
except:
    print("No gmail keys found")
    
con = imaplib.IMAP4_SSL(config.imap_url, "993")  
con.login(config.user_name, config.password)  
con.select('Inbox')

def query_msg_ids(subject_tag = None, sender = None, unseen = True):
    # subject_tag = "ECOLOG"
    # unseen = False
    # sender = "noreply@findajob-mail.agu.org"
    prior_date = datetime.date.today() - datetime.timedelta(days = 7)
    prior_date = prior_date.strftime("%d-%b-%Y")

    if sender is not None:
        if unseen == False:
            typ, data = con.search(None, '(FROM ' + sender + ' SINCE "' + prior_date + '")')
        else:
            typ, data = con.search(None, '(FROM "' + sender, '"' + ' UNSEEN)')
    else: # filtering by subject
        if unseen == False:
            typ, data = con.search(None, '(SUBJECT ' + subject_tag + ' SINCE "' + prior_date + '")')
        else:
            typ, data = con.search(None, '(SUBJECT "' + subject_tag, '"' + ' UNSEEN)')
    msg_ids = [int(x) for x in data[0].split()]
    return msg_ids

def pull_msg(id):
    typ, data = con.fetch(str(id),'(RFC822)')
    msg = email.message_from_string(str(data[0]))
    return msg

def pull_msg_content_ecolog(msg_raw):
    re_subject = re.compile('(?<=Subject: \[ECOLOG-L\] ).*(?=List-Subscribe)')
    subject = re_subject.findall(msg_raw.get_payload())
    subject = [x.replace("\\r\\n","") for x in subject]
    if(len(subject) == 0):
        subject = ["error"]
    # print(subject)

    re_body = re.compile('(?<=Content-Type: text\\/plain; charset="us-ascii"\\\\r\\\\nContent-Transfer-Encoding: quoted-printable).*?(?=Manage your Group settings)')
    body = re_body.findall(msg_raw.get_payload())
    if len(body) == 0:
        re_body = re.compile('(?<=Content-Type: text\\/plain; charset="iso-8859-1"\\\\r\\\\nContent-Transfer-Encoding: ).*?(?=Manage your Group settings)')
        body = re_body.findall(msg_raw.get_payload())
    if len(body) == 0:
        re_body = re.compile('(?<=Content-Type: text\\/plain; charset="UTF-8"\\\\r\\\\nContent-Transfer-Encoding: quoted-printable).*?(?=Manage your Group settings)')
        body = re_body.findall(msg_raw.get_payload())
    if len(body) == 0:
        re_body = re.compile('(?<=Content-Type: text\\/plain; charset="utf-8"\\\\r\\\\nContent-Transfer-Encoding: quoted-printable).*?(?=Manage your Group settings)')
        body = re_body.findall(msg_raw.get_payload())
    if len(body) == 0:
        re_body = re.compile('(?<=Content-Type: text\\/plain; charset="UTF-8"\\\\r\\\\nContent-Transfer-Encoding: ).*?(?=Manage your Group settings)')
        body = re_body.findall(msg_raw.get_payload())
    if len(body) == 0:
        re_body = re.compile('(?<=Content-Type: text\\/plain; charset="Windows-1252"\\\\r\\\\nContent-Transfer-Encoding: ).*?(?=Manage your Group settings)')
        body = re_body.findall(msg_raw.get_payload())
    if len(body) == 0:
        body = "error"

    url = utils.extract_url(body)

    # some urls have an equal sign...
    body = [x.replace("=","") for x in body]    
    body = [x.replace("~","") for x in body]    
    body = [x.replace("--","") for x in body]

    return [subject, body, url]

def pull_ecolog(unseen = True):
    # unseen = False
    subject_tag = "ECOLOG"
    msg_ids = query_msg_ids(subject_tag = subject_tag, unseen = unseen)
    # msg_ids = query_msg_ids(subject_tag, unseen = False)
    # msg_ids = msg_ids[10:20]

    subject_list = []
    body_list = []
    url_list = []

    global id
    for id in msg_ids:
        # id = msg_ids[2]
        # np.where(np.array(msg_ids) == 33)        
        # print(id)
        msg_raw = pull_msg(id)
        # if id == 959:
        #     breakpoint()
        msg_subject, msg_body, msg_url = pull_msg_content_ecolog(msg_raw)

        subject_list.append(msg_subject[0])
        body_list.append(msg_body[0])
        url_list.append(msg_url)
    
    res = pd.DataFrame({'subject': subject_list, 'body': body_list, 'url': url_list})        
    res['source'] = '[ECOLOG]'
    res['subject'] = res['subject'] + ' | ' + \
        res['url'] + ' | ' + res['source']

    if len(res) > 0:
        res = utils.filter_limno(res)

    return res

## agu
# sender = "noreply@findajob-mail.agu.org"
# msg_ids = query_msg_ids(sender = sender, unseen = False)
# subject_list = []
# body_list = []
# url_list = []
## for id in msg_ids:
# id = msg_ids[1]
# print(id)
# msg_raw = pull_msg(id)
# msg_subject, msg_body, msg_url = pull_msg_content_agu(msg_raw)        

# subject_list.append(msg_subject[0])
# body_list.append(msg_body[0])
# url_list.append(msg_url)