#-*-coding:utf-8-*-

from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Groups(models.Model):

    '''主机分组表'''

    groupid = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    internal = models.IntegerField(null=True, default=0)
    flags = models.IntegerField(null=True, default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '主机组'
        verbose_name_plural = '主机组'


class Templates(models.Model):

    '''模版表'''
    templateid = models.BigIntegerField(primary_key=True)
    host = models.CharField(max_length=128)
    name = models.CharField(max_length=128,null=True,blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '模版表'
        verbose_name_plural = '模版表'


class Proxy(models.Model):

    proxyid = models.BigIntegerField(primary_key=True)
    host = models.CharField(max_length=128,blank=True, null=True)
    name = models.CharField(max_length=128,blank=True, null=True)

    def __unicode__(self):
        return self.host

    class Meta:
        verbose_name = '代理'
        verbose_name_plural = '代理'


class Hosts(models.Model):

    '''主机表'''
    hostid = models.BigIntegerField(primary_key=True)
    proxyid  = models.ForeignKey('Proxy', null=True,blank=True)
    host = models.CharField(max_length=128)
    status = models.IntegerField()
    name = models.CharField(max_length=128)
    flags = models.IntegerField()
    interfaces = models.GenericIPAddressField()
    groupid = models.ForeignKey('Groups', blank=True, null=True)
    templateid = models.ForeignKey('Templates', blank=True, null=True)
    templatenum = models.IntegerField()
    itemsnum = models.IntegerField()
    triggernum = models.IntegerField()
    graphsnum = models.IntegerField()
    screensid = models.IntegerField()
    applicationsnum = models.IntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = '主机表'
        verbose_name = '主机表'


class Items(models.Model):
    '''监控项'''
    itemid = models.BigIntegerField(primary_key=True)
    type = models.IntegerField()
    hostid = models.ForeignKey('Hosts')
    name = models.CharField(max_length=255)
    key = models.CharField(db_column='key_',max_length=255)
    delay = models.IntegerField()
    history = models.IntegerField()
    trends = models.IntegerField()
    status = models.IntegerField()
    lastclock = models.IntegerField()
    data_type = models.IntegerField()

    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = '监控项'
        verbose_name_plural = '监控项'


class Triggers(models.Model):

    triggerid = models.BigIntegerField(primary_key=True)
    expression = models.CharField(max_length=2048)
    description = models.CharField(max_length=255)
    status = models.IntegerField()
    comments = models.TextField()
    templateid = models.ForeignKey('Templates')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = '触发器'
        verbose_name = '触发器'


class Graphs(models.Model):

    '''绘图'''
    graphid = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '绘图'
        verbose_name_plural = '绘图'



