#-*-coding:utf-8-*-
try: import httplib
except ImportError:
    import http.client as httplib

import sys
import urllib
import urllib2
import time
import random
import json
import itertools
import mimetypes
import base64
import hmac
import uuid
import traceback
from hashlib import sha1
import datetime


class PushAliCdn:

    def __init__(self, url, access_id, access_secret):
        self.access_id = access_id
        self.access_secret = access_secret
        self.url = url
    ##签名
    def sign(self,accessKeySecret, parameters):
        sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
        canonicalizedQueryString = ''
        for (k,v) in sortedParameters:
            canonicalizedQueryString += '&' + self.percent_encode(k) + '=' + self.percent_encode(v)

        stringToSign = 'GET&%2F&' + self.percent_encode(canonicalizedQueryString[1:]) #使用get请求方法

        h = hmac.new(accessKeySecret + "&", stringToSign, sha1)
        signature = base64.encodestring(h.digest()).strip()
        return signature

    def percent_encode(self,encodeStr):
        encodeStr = str(encodeStr)
        res = urllib.quote(encodeStr.decode(sys.stdin.encoding).encode('utf8'), '')
        res = res.replace('+', '%20')
        res = res.replace('*', '%2A')
        res = res.replace('%7E', '~')
        return res

    def make_url(self,params):
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        parameters = {
            'Format' : 'JSON',
            'Version': '2014-11-11',
            'AccessKeyId' : self.access_id,
            'SignatureVersion' : '1.0',
            'SignatureMethod' : 'HMAC-SHA1',
            'SignatureNonce' : str(uuid.uuid1()),
            'TimeStamp' : timestamp,
        }
        for key in params.keys():
            parameters[key] = params[key]

        signature = self.sign(self.access_secret,parameters)
        parameters['Signature'] = signature
        url = self.url + "/?" + urllib.urlencode(parameters)
        return url

    def do_request(self,params):
        url = self.make_url(params)
        request = urllib2.Request(url)
        try:
            conn = urllib2.urlopen(request)
            response = conn.read()
        except urllib2.HTTPError, e:
            return e.read().strip()
        try:
            obj = json.loads(response)
        except ValueError, e:
            return SystemExit(e)
        return obj

def UpdateCdn(urls):
    if urls is None:
        return None
    else:
        count = 0
        for i in urls:
            f = PushAliCdn("https://cdn.aliyuncs.com", 'LTAItjqH3pa6zrLC', 'ALNgaQAA4xhQKHS5pOOmpaQ31aeAhE')
            user_params = {'Action': 'RefreshObjectCaches', 'ObjectPath': '%s' % i, 'ObjectType': 'Directory'}
            res = f.do_request(user_params)
            try:
                if res.has_key('RefreshTaskId'):
                    result = res['RefreshTaskId'] + ' ' + '阿里Cdn目录刷新成功，在5分钟内同步到全部节点！'.encode('utf-8')
                    count += 1
                    print result, 444, 555
                    return result
                else:
                    result = res['Message'] + ' ' + res['Code'] + ' ' + '刷新失败， 请联系该项目运维同学！'.encode('utf-8')
                    print result, 666, 777
                    return result
            except Exception, e:
                result = 'Cdn刷新失败!'
                print result
                return result