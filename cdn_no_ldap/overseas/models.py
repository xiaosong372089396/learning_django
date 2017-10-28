#-*- coding:utf-8 -*-

from __future__ import unicode_literals

from django.db import models

class  overseas(models.Model):
    date = models.CharField(max_length=32, verbose_name="时间")
    username = models.CharField(max_length=32, verbose_name="用户")
    ip = models.GenericIPAddressField(protocol="ipv4", db_index=True, null=True, verbose_name="IP地址")

    class Meta:
        verbose_name = '海外缓存'
        verbose_name_plural = '海外缓存'
        ordering = ['id']

    def __unicode__(self):
        return self.date
