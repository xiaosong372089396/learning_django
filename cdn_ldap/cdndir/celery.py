#-*- coding:utf-8 -*-

from __future__ import absolute_import
import os
from celery import  Celery
from django.conf import settings
import logging
import traceback
import requests
logger = logging.getLogger("cdndir")


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cdndir.settings')
app = Celery('cdndir')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
