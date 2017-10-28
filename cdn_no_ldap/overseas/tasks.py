#-*- coding:utf-8 -*-

from celery import shared_task
from overseas.remote_api import remote
from cdndir.celery import  app

@app.task
def remoteAsync():
    remote()
    print 'remote_update'

