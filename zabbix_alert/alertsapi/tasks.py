#-*- coding:utf-8 -*-

from  __future__ import absolute_import
from Free.celery import app
from celery import shared_task
from alertsapi.Daemon_Rabbit  import QueueAPI
import sys
reload(sys)
sys.setdefaultencoding('utf8')


Rabbit = QueueAPI()

@app.task(bind=True)
def update_login(self):
    Rabbit.Consumers()
    print 'update rabbit login connection'


@app.task(bind=True)
def update_receive(self):
    Rabbit.receive()
    print 'update receive'