#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json

url = 'http://127.0.0.1:5000/mobile_message/api/v1.0/tasks'

data = {'username': '', 'password': '', 'mobile': '', 'content': ''}

headers = {'content-type': 'application/json',
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}

result = requests.post(url, data=json.dumps(data), headers=headers)

print result.text
