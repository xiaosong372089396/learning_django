#-*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib
import urllib2
from socket import timeout
import traceback
import json


class GetTxCdn(object):

    def __init__(self, prefix, user, password, output):
        self.user = user
        self.password = password
        self.output = output
        self.prefix = prefix

    def get_pad(self):
        rest_fun = "padList"
        data = {
            'user' : self.user,
            'pass' : self.password,
            'output': self.prefix
        }
        req = urllib2.Request(self.prefix + rest_fun, urllib.urlencode(data).encode('utf-8'))
        res = urllib2.urlopen(req, timeout=300)
        if res.getcode() == 200:
            res_data = res.read().decode('utf-8')
            print res_data
        else:
            print res.getcode()

class PushTxCdn(object):

    def __init__(self, prefix, user, password, output, pad, mailto, uri_list):
        self.prefix = prefix
        self.user = user
        self.password = password
        self.output = output
        self.pad = pad
        self.mailto = mailto
        self.uri_list = uri_list

    def purage_data(self):
        rest_fun = 'doPurge'
        data = {
            'user' : self.user,
            'pass' : self.password,
            'output': self.output,
            'pad': self.pad,
            'type': 'item',  #wildcard,all
            'path': self.uri_list,
            'mailTo': self.mailto
        }
        req = urllib2.Request(self.prefix + rest_fun, urllib.urlencode(data, doseq=True).encode('utf-8'))
        res = urllib2.urlopen(req, timeout=300)
        if res.getcode() == 200:
            res_data = res.read().decode('utf-8')
            return res_data
        elif res.getcode() == 400:
            res_data = res.read().decode('utf-8')
            return res_data
        elif res.getcode() == 403:
            res_data = res.read().decode('utf-8')
            return res_data
        elif res.getcode() == 404:
            res_data = res.read().decode('utf-8')
            return res_data
        elif res.getcode() == 500:
            res_data = res.read().decode('utf-8')
            return res_data
        elif res.getcode() == 509:
            res_data = res.read().decode('utf-8')
            return res_data
        else:
            return (res.getcode())




