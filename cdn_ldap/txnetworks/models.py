#-*- coding:utf-8 -*-

from __future__ import unicode_literals

from django.db import models

class Txpad(models.Model):
    urlpad = models.CharField(max_length=50,null=True, verbose_name='热更刷新地址')

    class Meta:
        verbose_name = '热更地址'
        verbose_name_plural = '热更地址'
        ordering = ['id']

    def __unicode__(self):
        return  self.urlpad

class  txnetwork(models.Model):
    date = models.CharField(max_length=32, null=True ,verbose_name="时间")
    username = models.CharField(max_length=32,null=True ,verbose_name="用户")
    ip = models.GenericIPAddressField(protocol="ipv4", db_index=True, null=True, verbose_name="IP地址")
    flushurl = models.URLField(null=True,verbose_name="热更地址")
    flushpath = models.CharField(max_length=20, null=True ,verbose_name="热更路径")

    class Meta:
        verbose_name = '同心万点'
        verbose_name_plural = '同心万点'
        ordering = ['id']

    def __unicode__(self):
        return self.date
