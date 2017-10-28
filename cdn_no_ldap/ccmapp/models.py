#-*- coding:utf-8 -*-

from __future__ import unicode_literals

from django.db import models

class  CCMrecord(models.Model):
    date = models.CharField(max_length=32, verbose_name="时间")
    username = models.CharField(max_length=32, verbose_name="用户")
    ip = models.GenericIPAddressField(protocol="ipv4", db_index=True, null=True, verbose_name="IP地址")
    active = models.TextField(verbose_name="刷新内容")

    class Meta:
        verbose_name = '网宿Cdn'
        verbose_name_plural = '网宿Cdn'
        ordering = ['id']

    def __unicode__(self):
        return self.date
