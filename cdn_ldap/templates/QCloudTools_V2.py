import os
import hashlib
import urllib
import requests
import binascii
import hmac
import copy
import random
import sys
import time
from pprint import pprint
from optparse import OptionParser
from requests.packages.urllib3.exceptions import InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
reload(sys)
sys.setdefaultencoding("utf-8")
import json

url='https://cdn.api.qcloud.com/v2/index.php'
secretId='AKIDIUXO3V6puqhUIyrD5mHcnmbFgvypivBr'
secretKey='c2GNMDxZ7vcCf0DLLD7rSt9C3iBVfcNw'
requestHost= 'cdn.api.qcloud.com'
requestUri='/v2/index.php'
method = "POST"
params = {
                'Action':'RefreshCdnDir',
                # 'Action':'DescribeCdnHosts',
                'Nonce': random.randint(1, sys.maxint),
                # 'Nonce': 13029,
                'Timestamp': int(time.time()),
                # 'Timestamp': 1463122059,
                'SecretId' : secretId,
                # 'offset': 0,
                # 'limit':10
                }

class Sign(object):
    def __init__(self, secretId, secretKey):
        self.secretId = secretId
        self.secretKey = secretKey

    def make(self, requestsHost, requestsUri, params, method = 'POST'):
        a1 = "&".join(k.replace("_",".") + "=" + str(params[k]) for k in sorted(params.keys()))
        print a1
        srcStr = method.upper() + requestHost + requestUri + '?' + "&".join(k.replace("_",".") + "=" + str(params[k]) for k in sorted(params.keys()))
        hashed = hmac.new(self.secretKey, srcStr, hashlib.sha1)
        return binascii.b2a_base64(hashed.digest())[:-1]
sign = Sign(secretId,secretKey)

a5 = {'a2':'http://update.xlgymj.cn/', 'a3':'http://update.xlsymj.com/', 'a4':'https://www.ixianlai.com/'}
Uri = a5.values()
for i in Uri:
    params['key'] = i
params['Signature'] = sign.make(requestsHost, requestUri, params, method)
urls = 'https://%s%s' % (requestHost, requestUri)
print urls
if method.upper == 'GET':
    req = requests.get(url,  params=params, timeout=20, verify=False)
else:
    req = requests.post(url, params=params, files={}, timeout=10, verify=False)
