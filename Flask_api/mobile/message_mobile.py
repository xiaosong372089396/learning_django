# -*- coding:utf-8 -*-


import hashlib
import requests
import sys


def Message(mobile,content):
    url = 'http://msgapi.qq.com/smsgateway/msg/serverSendMsg'
    key = ''
    tel = mobile
    cst_id = '55555'
    md5 = tel + cst_id + key
    hash = hashlib.md5()
    hash.update(md5.encode('utf-8'))
    sign = hash.hexdigest()
    payload = {'cst_id': cst_id, 'sign': sign, 'tel': tel, 'content': content}

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
    ret = requests.post(url, data=payload,headers=headers)
    return (ret.text)




"""
if __name__ == "__main__":
    mobile = sys.argv[1]
    content = sys.argv[3]
    if '32000' in str(content) or '1988' in str(content):
        pass
    else:
        Message(mobile,content)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
"""