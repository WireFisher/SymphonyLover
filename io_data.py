#!/usr/bin/env python3

from lxml import etree

def init(filename):
    global tree, root, mail, symp
    try:
        tree = etree.parse(filename)
        root = tree.getroot()
        for child in root:
            if child.tag == 'mail':
                mail = child
            elif child.tag == 'symp':
                symp = child
    except IOError:
        print("data.xml Not Found. Initializing, records and e-mail info\(password included\) will be saved in data.xml")
        root = etree.Element('data')
        mail = etree.SubElement(root, 'mail')
        symp = etree.SubElement(root, 'symp')
        tree = etree.ElementTree(root)

def exist(iden):
    for child in symp:
        if iden == child.get('id'):
            return True
    return False

def insert(iden, url, title):
    new_event = etree.SubElement(symp, 'event')
    new_event.set('id', iden)
    new_event.set('url', url)
    new_event.text = title

def set_mail(host, user, passwd, receivers):
    mail.set('host', host)
    mail.set('user', user)
    mail.set('passwd', passwd)
    for receiv in receivers:
        receiver = etree.SubElement(mail, 'receiver')
        receiver.text = receiv

def get_mail():
    mailinfo = [mail.get('host'), mail.get('user'), mail.get('passwd')]
    return mailinfo

def get_receivers():
    receivers = []
    for receiver in mail:
        receivers.append(receiver.text)
    return receivers

def save(filename):
    tree.write(filename, pretty_print=True, encoding='utf-8')

if __name__ == '__main__':    
    name = 'test2.xml'
    init(name)
    #title = 'e'
    #insert('2649', 'http://www.hall.tsinghua.edu.cn/info/yc/2649', title)
    #print(exist('2649'))
    #set_mail('smtp.host.com', 'username', 'password', ['1@mail.com','2@mail.com'])
    [host, user, passwd] = get_mail()
    print(host, user, passwd)
    reces = get_receivers()
    print(reces)
    #save(name)
