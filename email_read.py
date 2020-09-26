# https://www.geeksforgeeks.org/python-fetch-your-gmail-emails-from-a-particular-user/

import email
import imaplib
import re
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

type, data = con.search(None, 'ALL')
mail_ids = data[0]

id_list = mail_ids.split()   
first_email_id = int(id_list[0])
latest_email_id = int(id_list[-1])

typ, data = con.fetch(str(2),'(RFC822)')
msg = email.message_from_string(str(data[0]))

## subject
# extract between: 'Subject:' and 'List-Subscribe:'
re_subject = re.compile('(?<=Subject: ).*(?=List-Subscribe)')
subject = re_subject.findall(msg.get_payload())

re_body = re.compile('(?<=Content-Type: text\/plain; charset="us-ascii"\\\\r\\\\nContent-Transfer-Encoding: quoted-printable).*?(?=\\\\r\\\\n\\\\r\\\\n\\\\r\\\\n\\\\r')
body = re_body.findall(msg.get_payload())
body = [x.replace("\\r\\n","") for x in body]
body = [x.replace("~","") for x in body]
body = [x.replace("=","") for x in body]
body = [x.replace("--","") for x in body]

body
