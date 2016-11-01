#!/usr/bin/env python3

import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_mail(host, user, passwd, subject, receivers, content):
    
    p = host.find('.')
    sender = user + '@' + host[p+1:]
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = sender
    message['To'] = ','.join(receivers)
    message['Subject'] = subject
    
    try:
        s = smtplib.SMTP()
        s.connect(host, 25)
        s.login(user, passwd)
        s.sendmail(sender, receivers, message.as_string())
        print("E-mail delivered")
    except smtplib.SMTPException:
        print("Error: Can not delivere e-mail properly")

if __name__ == '__main__':
    host = 'smtp.xxx.com'
    user = 'xxx'
    passwd = 'xxx'
    receivers = ['xxx@xxx.cn', 'ooo@ooo.com']
    sender = 'xxx@xxx.com'
    subject = '标题测试'
    content = '我是正文'
    send_mail(host, user, passwd, subject, receivers, content)
