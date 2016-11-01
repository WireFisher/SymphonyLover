#!/usr/bin/env python3

import requests
import io_data
import mail
import getpass
import os
import time

def browse(url, keywords):
    r = requests.get(url)
    result = r.text

    for keyword in keywords:
        p_middle = result.find(keyword)
        while p_middle != -1:
            p_end = result.find("</a>", p_middle)
            p_start = result.rfind("<a ", 0, p_middle)
            trim = result[p_start:p_end]
            keyword_link = ['/info/pwzx_hdap/','/info/yc/']
            for key in keyword_link:
                p_key = trim.find(key)
                if (p_key != -1):
                    idnum = trim[p_key+len(key):p_key+len(key)+4]
                    link = 'http://www.hall.tsinghua.edu.cn' + key + idnum
                    break
            p_text = trim.find(">")
            title = trim[p_text+1:]
            p_middle = result.find(keyword, p_middle+1)
            if not io_data.exist(idnum):
                io_data.insert(idnum, link, title)
                print("-"*21 + " New record added.")
                [host, user, passwd] = io_data.get_mail()
                reces = io_data.get_receivers()
                subject = "交响音乐会有新演出更新"
                content = "演出名称：" + title + "\n演出链接：" + link
                mail.send_mail(host, user, passwd, subject, reces, content)
                
def initial(filepath):
    io_data.init(filepath)
    rece_not_empty = 0
    for child in io_data.mail:
        if len(child.text) != 0:
            rece_not_empty = 1

    if not ( bool(io_data.mail.get('host')) & bool(io_data.mail.get('user')) & bool(io_data.mail.get('passwd')) & rece_not_empty):
        print("Mail info missing, please reset.")
        in_host = input("Hostname:")
        in_user = input("Username:")
        in_passwd = getpass.getpass("Password:")
        in_receivers_str = input("Receivers(comma-delimited):")
        in_receivers = in_receivers_str.split(',')
        io_data.set_mail(in_host, in_user, in_passwd, in_receivers)

if __name__ == '__main__':
    print("[%s] Job start: " % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    url = 'http://www.hall.tsinghua.edu.cn/columnEx/pwzx_hdap/yc/1'
    keywords = ["交响"]
    path = os.path.dirname(os.path.abspath(__file__)) + "/data.xml"
    initial(path)
    browse(url, keywords)
    io_data.save(path)
    print("[%s] Job stop normally." % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
