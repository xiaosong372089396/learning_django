#-*- coding:utf-8 -*-

import django
import os
import time
from Free import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Free.settings")
django.setup()

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import pika
import traceback
from alertsapi.models import Alerts
from alertsapi.models import Alert_User
from alertsapi import Screens
import time
import collections
import MeaageMobile
import gc
import logging
logger = logging.getLogger("free")



class  QueueAPI(object):
    def  __init__(self, username='admin', password='xianlai'):
        self.username = username
        self.password = password

    def  Consumers(self):
        try:
            self.credentials = pika.PlainCredentials(username=self.username, password=self.password)
            self.connection  = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1', 5672, '/', self.credentials))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue='zabbix', durable=True)    #声明队列持久化
        except Exception,e:
            print traceback.format_exc(),e


    def  callback(self, ch, method, properties, body):
        try:
            Calculate = dict()
            self.body = body
            logfile = str(self.body).split('|')
            hosts , infos, statuss, severitys, timess = logfile[0].split(':'), logfile[1].split(':'), logfile[2].split(':'), logfile[3].split(':'), logfile[4].split()
            timess[0], timess[1], timess[2] = timess[0].strip("'"),timess[1].strip("'"),timess[2].strip("'")
            timess[1] = timess[1].replace('.','-')
            mtime = timess[1] + ' ' + timess[2]
            Calculate['host'], Calculate['info'], Calculate['status'], Calculate['severity'], Calculate['time'] = hosts[1], infos[1], statuss[1], severitys[1], mtime
            AlertsINFO = Alerts.objects.create(hostname = Calculate['host'], level=Calculate['severity'], message=Calculate['info'], times=Calculate['time'], status=Calculate['status'])
            AlertsINFO.save()
            hostname, message, status, level = Screens.HostName(mtime), Screens.Message(mtime), Screens.Status(mtime), Screens.Level(mtime)
            host_send, message_send, status_send, level_send = Screens.Host_send(hostname), Screens.Message_send(message), Screens.Status_send(status),Screens.Level_send(level)
            values = '主机：' + '\n'+ '[ ' +  str(host_send) + ' ]' +  '\n' + '信息：' + str(message_send) + '\n' + '状态：' + str(status_send) + '\n'+  '时间：' + mtime + '\n' + '_________'.encode('utf-8')
            #告警用户
            v = Alert_User.objects.filter().values('mobile')
            for i in v:
                for key,mobile in i.items():
                    MeaageMobile.Message(mobile,values)
                    print mobile, '\n', values
            gc.collect()
        except Exception,e:
            print  traceback.format_exc(),e

    def   receive(self):
        try:
            self.channel.basic_consume(self.callback ,queue='zabbix', no_ack=True)   #no_ack=True表示在回调函数中不需要发送确认标识
            print ('[*], 持续消费队列动作')
        except Exception,e:
            logger.error(traceback.format_exc())
            print traceback.format_exc(),e

        #开始接收信息并进入阻塞状态， 列队里有信息才会调用callback进行处理， 按CTRL+C退出
        self.channel.start_consuming()
        import time
        time.sleep(1)
        self.connection.close()

