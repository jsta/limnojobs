# https://www.geeksforgeeks.org/python-fetch-your-gmail-emails-from-a-particular-user/

import email
import imaplib
import re
import pandas as pd
import pkg_resources
# import base64
# import html2text
# import mailparser
from utils import filter_limno

try:
    import config
except:
    print("No gmail keys found")
    
con = imaplib.IMAP4_SSL(config.imap_url, "993")
  
# logging the user in 
con.login(config.user_name, config.password)
  
# calling function to check for email under this label 
con.select('Inbox')

def query_msg_ids(subject_tag):
    # subject_tag = "ECOLOG"
    typ, data = con.search(None, 'SUBJECT ' + subject_tag)
    msg_ids = [int(x) for x in data[0].split()]
    return msg_ids

def pull_msg(id):
    typ, data = con.fetch(str(id),'(RFC822)')
    msg = email.message_from_string(str(data[0]))
    return msg

def pull_msg_content(msg_raw):
    re_subject = re.compile('(?<=Subject: ).*(?=List-Subscribe)')
    subject = re_subject.findall(msg_raw.get_payload())

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
        body = "error"

    body = [x.replace("\\r\\n","") for x in body]
    body = [x.replace("~","") for x in body]
    body = [x.replace("=","") for x in body]
    body = [x.replace("--","") for x in body]

    return [subject, body]

def pull_ecolog():
    subject_tag = "ECOLOG"
    msg_ids = query_msg_ids(subject_tag)

    subject_list = []
    body_list = []

    for id in msg_ids:
        # id = msg_ids[24]
        # np.where(np.array(msg_ids) == 33)
        print(id)
        msg_raw = pull_msg(id)
        msg_subject, msg_body = pull_msg_content(msg_raw)

        subject_list.append(msg_subject[0])
        body_list.append(msg_body[0])

    res = pd.DataFrame({'subject': subject_list, 'body': body_list})
    res = filter_limno(res)

    return res
