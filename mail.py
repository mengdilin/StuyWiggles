#!/usr/bin/env python
# -*- coding: utf-8 -*-
from email.header    import Header
from email.mime.text import MIMEText
from getpass         import getpass
from smtplib         import SMTP_SSL

login, password = 'mengdilin95@gmail.com', getpass('Enter Password:')

def msg(body,subject,mail):
# create message
    msg = MIMEText(body, _charset='utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = login
    msg['To'] = mail
# send it via gmail
    s = SMTP_SSL('smtp.gmail.com', 465, timeout=10)
    s.set_debuglevel(0)
    try:
        s.login(login, password)
        s.sendmail(msg['From'], msg['To'], msg.as_string())
    finally:
        s.quit()

if __name__=="__main__":
    msg("omggg this is a sex body","yep this better works as a subject","mengdilin@aol.com")
