# https://www.geeksforgeeks.org/python-fetch-your-gmail-emails-from-a-particular-user/

import email
import imaplib
import re
import pandas as pd
import pkg_resources
# import base64
# import html2text
# import mailparser

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

    body = [x.replace("\\r\\n","") for x in body]
    body = [x.replace("~","") for x in body]
    body = [x.replace("=","") for x in body]
    body = [x.replace("--","") for x in body]

    return [subject, body]

def filter_limno(df):
    r"""Filter limnology themed jobs from a pandas DataFrame.
    :param df: pandas DataFrame with 'subject' and 'body' columns
    """

    keywords = pd.read_csv(pkg_resources.resource_filename('limnojobs',
                                                           'keywords.csv'))
    filter_for = keywords['filter_for'].tolist()
    filter_for = [x for x in filter_for if str(x) != 'nan']
    filter_against = keywords['filter_against'].tolist()
    filter_against = [x for x in filter_against if str(x) != 'nan']

    # df = res
    df = df.reset_index()    
    # df = df.iloc[0:2]

    has_limno_subject = df['subject'].str.contains('|'.join(filter_for),
                                               case = False)
    has_limno_body = df['body'].str.contains('|'.join(filter_for),
                                                   case = False)

    # save matching filter_for here
    is_limno = pd.DataFrame([has_limno_subject, has_limno_body]) \
        .transpose() \
        .sum(axis = 1) > 0

    df = df[is_limno]

    has_junk_subject = ~df['subject'].str.contains('|'.join(filter_against),
                                                   case = False)
    has_junk_body = ~df['body'].str.contains('|'.join(filter_against),
                                               case = False)

    # save matching filter_against here
    # if len(df.index) > 0:
    #     filter_against = keywords['filter_against'][
    #         keywords['filter_against'].apply(
    #             lambda x: df['body'].
    #             str.contains(x, case = False)).iloc[:, 0]]

    not_junk = pd.DataFrame([has_junk_subject, has_junk_body]) \
        .transpose() \
        .sum(axis = 1) == 2

    return df[not_junk]# ,
            #"filter_against": filter_against}

#####

subject_tag = "ECOLOG"
msg_ids = query_msg_ids(subject_tag)

subject_list = []
body_list = []

for id in msg_ids:
    # id = msg_ids[1]
    print(id)
    msg_raw = pull_msg(id)
    msg_subject, msg_body = pull_msg_content(msg_raw)

    subject_list.append(msg_subject[0])
    body_list.append(msg_body[0])

res = pd.DataFrame({'subject': subject_list, 'body': body_list})

res = filter_limno(res)

res.to_csv(subject_tag + ".csv")

