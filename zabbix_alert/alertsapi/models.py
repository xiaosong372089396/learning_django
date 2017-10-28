# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



class Alerts(models.Model):
    hostname = models.CharField(max_length=50,verbose_name='主机名称', blank=True)
    message  = models.CharField(max_length=50,verbose_name='告警信息', blank=True)
    status   = models.CharField(max_length=50,verbose_name='当前状态', blank=True)
    level    = models.CharField(max_length=50,verbose_name='告警级别', blank=True)
    times    = models.CharField(max_length=50,verbose_name='告警时间', blank=True)


    class Meta:
        verbose_name = '告警信息'
        verbose_name_plural = '告警信息列表'
        ordering = ['id']

    def __unicode__(self):
        return  self.hostname



class  Alert_User(models.Model):
    username = models.CharField(max_length=50, verbose_name='告警用户', blank=True)
    mobile   = models.CharField(max_length=50, verbose_name='手机号', blank=True)

    class Meta:
        verbose_name = '短信告警'
        verbose_name_plural = '短信告警通知'
        ordering = ['id']

    def __unicode__(self):
        return self.username
