#-*- coding:utf-8 -*-

import hashlib,requests,sys

def Message(mobile,content):
    url = 'http://msgapi.ixianlai.com/smsgateway/msg/serverSendMsg'
    key = ''
    tel = mobile
    cst_id = '55555'
    md5 = tel + cst_id + key
    hash = hashlib.md5()
    hash.update(md5.encode('utf-8'))
    sign = hash.hexdigest()
    payload = {'cst_id': cst_id, 'sign': sign, 'tel': tel, 'content': content}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
    ret = requests.post(url, data=payload,headers=headers)
    return (ret.text)


"""
if __name__ == "__main__":
    #移动
    mobile = sys.argv[1]
    #内容
    content = sys.argv[3]
    if '32000' in str(content):
        pass
    else:
        Message(mobile,content)
"""