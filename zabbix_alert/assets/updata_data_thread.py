# coding=utf-8
# !/usr/bin/python
import threading
import time
import Queue
import traceback
import requests
import logging
from Free.settings import SELF_IP
from django.conf import settings

q = Queue.Queue(0)
logger = logging.getLogger("free")


#请求url
def send_request(url):
    try:
        headers = {'content-type': 'application/json'}
        requests.get(url)
        requests.keep_alive = False
    except Exception, e:
        print traceback.format_exc()
        logger.error('send request error ,the url is : ' + url + traceback.format_exc())


class MyThread(threading.Thread):

    def __init__(self, input, worktype, url, delay= 5):
        self.url = url
        self.delay = delay
        self._jobq = input
        self._work_type = worktype
        threading.Thread.__init__(self)

    def run(self):

        count = 0
        while True:
            if self._jobq.qsize() > 0:
                while True:
                    try:
                        time.sleep(self.delay)
                        count = count + 1
                        headers = {'content-type': 'application/json'}
                        requests.get(self.url)
                        requests.keep_alive = False
                    except Exception, e:
                        print traceback.format_exc()


#起线程开始不断调用更新阿里云服务器
def update_data():
    url = SELF_IP + "/assets/update_data/"
    try:
        for i in range(1):
            q.put(i) 
        for x in range(1):
            MyThread(q, x, url).start()
    except Exception, e:
        logger.error("updata aliyun :" + traceback.format_exc())


#起进程开始不断调用腾讯云服务器
def update_qcloud():
    url = SELF_IP + "/assets/update_qcloud/"
    try:
        for i in range(1):
            q.put(i) 
        for x in range(1):
            MyThread(q, x, url, delay=10).start()
    except Exception, e:
        logger.error("update qcloud:" + traceback.format_exc())


#处理阿里云和腾讯云的数据库更新
def deal_rds():
    url = SELF_IP + '/assets/update_rds/'
    try:
        for i in range(1):
            q.put(i)
        for x in range(1):
            MyThread(q, x , url, delay=15).start()
    except Exception, e:
        logger.error('update rds: ' + traceback.format_exc())

#
# #日常轮询
# def deal_select():
#     url = SELF_IP + '/games/update_select/'
#     try:
#         for i in range(1):
#             q.put(i)
#         for x in range(1):
#             MyThread(q, x , url, delay=300).start()
#     except Exception, e:
#         logger.error('刘耀的select 出错了: ' + traceback.format_exc())
