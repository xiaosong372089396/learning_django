#-*- coding:utf-8 -*-

import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib
import urllib2
import time
import uuid
import traceback
import json
import requests


class PushWhiteCdn(object):

    def __init__(self):
        self.url = 'https://purge.qingcdn.com/purge/purge?' + 'token=' + ''
        self.headers = {"Content-Type": "application/json"}

    def Push(self,data):
        if data is None:
            return None
        Str = str(data)
        val = Str.split('\\n')
        dirurl = len(val)
        if dirurl == 1:
            value = str(data).strip('\\n').strip('[').strip(']').strip("u'").split('\\n')
            datas = {"urls": value, "type": "dir" }
            result = requests.post(self.url, data=json.dumps(datas), headers=self.headers)
            val = result.text
            vals = eval(val)
            for i in vals:
                num = int(i['id'])
                if  num > 0:
                    return  '提交成功 %s条, %s' % (dirurl,num)
                else:
                    return  '提交失败 %s条, %s' % (dirurl,num)
        else:
            value = str(data).strip('\\n').strip('[').strip(']').strip("u'").split('\\n')
            datas = {"urls": value, "type": "dir"}
            result = requests.post(self.url, data=json.dumps(datas),headers=self.headers)
            val =  result.text
            vals = eval(val)
            for i in vals:
                num = int(i['id'])
                if num > 0:
                    return '提交成功 %s条, %s' % (dirurl, num)
                else:
                    return '提交失败 %s条, %s' % (dirurl, num)