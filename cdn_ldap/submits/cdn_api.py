# -*- coding:utf-8 -*-

import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import random
import requests
import time
import hashlib
import binascii
import hmac
import platform
from django.shortcuts import HttpResponse
from requests.packages.urllib3.exceptions import InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
url='https://cdn.api.qcloud.com/v2/index.php'
secretId=''
secretKey=''
requestHost= 'cdn.api.qcloud.com'
requestUri='/v2/index.php'
method = "POST"


class Sign:
    def __init__(self, secretId, secretKey):
        self.secretId = secretId
        self.secretKey = secretKey
        self.params = {
                'Action':'RefreshCdnDir',
                'Nonce':  random.randint(1, sys.maxint),
                'Timestamp': int(time.time()),
                'SecretId' : secretId,
                }


    def make(self,requestHost, requestUri, params, method='POST'):
        a1="&".join(k.replace("_", ".") + "=" + str(params[k]) for k in sorted(params.keys()))
        srcStr = method.upper() + requestHost + requestUri + '?'+"&".join(k.replace("_", ".") + "=" + str(params[k]) for k in sorted(params.keys()))
        hashed = hmac.new(self.secretKey, srcStr, hashlib.sha1)
        return binascii.b2a_base64(hashed.digest())[:-1]

# sign = Sign(secretId,secretKey)
    def cdnrefresh(self,task):
        count=0
        # 传值过来的task 是一个list,222,333
        for value in task:
            if len(value.strip().strip('\n')) == 0:continue
            elif value.strip().strip('\n').startswith('#'):continue
            else:
                # key='dirs.'+str(count)
                # params[key]=value
                # count+=1
                for i in value.strip().split('\n'):
                    line1 = i.strip('\n').encode("ascii")
                    key = 'dirs.' + str(count)
                    self.params[key] = i
                    count += 1

        self.params['Signature'] = self.make(requestHost,requestUri,self.params,method)
        url = 'https://%s%s' % (requestHost, requestUri)
        req = requests.post(url, data=self.params, files={}, timeout=10,verify=False)
        res=req.text
        res=eval(res)
        if res['code'] == 0 and res['codeDesc'] == 'Success':
            if platform.platform().startswith('Windows'):
                # print  '刷新成功:%s条数据,在5分钟内同步到全部节点'.decode('utf-8').encode('gbk')%res['data']['count']
                result = '刷新成功:%s条数据,在5分钟内同步到全部节点'.decode('utf-8').encode('utf-8')%res['data']['count']  # 'encode('utf-8')'
                return result
            else:
                # print   '刷新成功:%s条数据,在5分钟内同步到全部节点'%res['data']['count']
                result = '刷新成功:%s条数据,在5分钟内同步到全部节点'%res['data']['count']
                return result
        else:
            if platform.platform().startswith('Windows'):
                # print '刷新失败!!!  请检查cdndir文件中的刷新路径'.decode('utf-8').encode('gbk'),1111
                # print '错误信息:'.decode('utf-8').encode('gbk'),res['message'].decode("unicode-escape"),222
                # print '错误类型:%s ,错误代码:%s'.decode('utf-8').encode('gbk')%(res['codeDesc'],res['code']),333
                result =  '刷新失败!!!  请检查cdndir文件中的刷新路径'.decode('utf-8').encode('utf-8'),'错误信息:'.decode('utf-8').encode('utf-8'),res['message'].decode("unicode-escape"),'错误类型:%s ,错误代码:%s'.decode('utf-8').encode('utf-8')%(res['codeDesc'],res['code'])
                return  result
            else:
                # print '刷新失败!!!  请检查cdndir文件中的刷新路径'
                # print '错误信息:',res['message'].decode("unicode-escape")
                # print '错误类型:%s ,错误代码:%s'%(res['codeDesc'],res['code'])
                result =   '刷新失败!!!  请检查cdndir文件中的刷新路径','错误信息:',res['message'].decode("unicode-escape"),'错误类型:%s ,错误代码:%s'%(res['codeDesc'],res['code'])
                return  result
