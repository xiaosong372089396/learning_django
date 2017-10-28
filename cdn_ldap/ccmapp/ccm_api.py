#-*- coding:utf-8 -*-

import hashlib
import requests
import sys
import os


class Ccm(object):

    def __init__(self):
        self.url = 'http://ccm.chinanetcenter.com/ccm/servlet/contReceiver'
        self.username = ''
        self.password = ''
        self.dir = ''
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}

    def ComBination(self, dirs):
        if dirs is None:
            return None
        Strs = str(dirs)
        val = Strs.split('\\n')
        dirurl = len(val)
        if  dirurl == 1:
            for i in dirs:
                md5 = self.username + self.password + i      #self.dir
                hash = hashlib.md5()
                hash.update(md5.encode('utf-8'))
                sign = hash.hexdigest()
                data = {'username': self.username, 'passwd': sign, 'dir': i }   #self.dir
                ret = requests.post(self.url, data=data, headers=self.headers)
                return ret.text + '成功提交地址数量：'+ '%s' % dirurl
        else:
            value = Strs.replace('\\n',';').strip('[').strip(']').strip("u'")
            md5 = self.username + self.password + value
            hash = hashlib.md5()
            hash.update(md5.encode('utf-8'))
            sign = hash.hexdigest()
            data = {'username': self.username, 'passwd': sign, 'dir': value }
            ret = requests.post(self.url, data=data, headers=self.headers)
            return ret.text +  '成功提交地址数量：' + '%s' % dirurl
