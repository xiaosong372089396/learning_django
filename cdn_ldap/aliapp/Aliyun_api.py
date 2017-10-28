#-*- coding:utf-8 -*-

import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib
import urllib2
import base64
import hmac
import hashlib
from hashlib import sha1
import time
import uuid
import httplib
import traceback
import json

class PushAliCdn(object):

    def __init__(self):
        self.cdn_server_address = "https://cdn.aliyuncs.com"
        self.access_key_id = ''
        self.access_key_secret = ''

    def percent_encode(self, us):
        enstr = str(us)
        res = urllib.quote(enstr.decode(sys.stdin.encoding).encode('utf8'), '')
        #坑，在Linux部署Django uWsgi sys.stdin.encoding 这里可以写死了
        #res = urllib.quote(enstr.decode('UTF-8').encode('utf8'), '')
        res = res.replace('+', '%20')
        res = res.replace('*', '%2A')
        res = res.replace('%7E', '~')
        return res

    def compute_signature(self,parameters, access_key_secret):
        sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
        canonicalizedQueryString = ''
        try:
            for k, v in sortedParameters:
                canonicalizedQueryString += '&' + self.percent_encode(k) + '=' + self.percent_encode(v)
        except Exception,e:
            print e
        stringToSign = 'GET&%2F&' + self.percent_encode(canonicalizedQueryString[1:])
        h = hmac.new(access_key_secret + '&', stringToSign, sha1)
        signature = base64.encodestring(h.digest()).strip()
        return signature

    def compose_url(self, user_params):
        timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        parameters = {'Format': 'JSON',
                      'Version': '2014-11-11',
                      'AccessKeyId': self.access_key_id,
                      'SignatureVersion': '1.0',
                      'SignatureMethod': 'HMAC-SHA1',
                      'SignatureNonce': str(uuid.uuid1()),
                      'TimeStamp': timestamp,
                      }
        for key in user_params.keys():
            parameters[key] = user_params[key]

        signature = self.compute_signature(parameters, self.access_key_secret)
        parameters['Signature'] = signature
        url = self.cdn_server_address + '/?' + urllib.urlencode(parameters)
        return url

    def  make_request(self, user_params):
        url = self.compose_url(user_params)
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
        for i in urls:
            f = PushAliCdn()
            user_params = {'Action': 'RefreshObjectCaches', 'ObjectPath': '%s' % i, 'ObjectType': 'Directory'}
            res = f.make_request(user_params)
            try:
                if  res.has_key('RefreshTaskId'):
                    result = res['RefreshTaskId'] + ' ' + '阿里Cdn目录刷新成功，在5分钟内同步到全部节点！'.encode('utf-8')
                    return result
                else:
                    result = res['Message'] + ' ' + res['Code'] + ' ' + '刷新失败， 请联系该项目运维同学！'.encode('utf-8')
                    print result
                    return  result
            except Exception,e:
                result = 'Cdn刷新失败!'
                print result
                return  result
            #{u'RefreshTaskId': u'1037502163', u'RequestId': u'0E6DA916-DD99-4A5F-9F70-A2B5BD2700D4'} 3333

#UpdateCdn(a)