# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Basemodel(models.Model):
    '''
       基础表(抽象类)
    '''
    name = models.CharField(max_length=32, verbose_name='名字')
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updatetime = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    note = models.TextField(default='', null=True, blank=True, verbose_name='备注')

    def __unicode__(self):
        return self.name  # 显示对象的名字

    class Meta:
        abstract = True  # 抽象类
        ordering = ['-id']  # 按id倒排

class InceptSql(Basemodel):
    SQL_STATUS = (
                        (-3, u'已回滚'),
                        (-2, u'已暂停'),
                        (-1, u'待执行'),
                        (0, u'已执行'),
                        (1, u'已放弃'),
                        (2, u'执行失败'),

    )
    sqlusers = models.ManyToManyField(User)
    commiter = models.CharField(max_length=20)  # 提交人
    sqlcontent = models.TextField(blank=True, null=True)  # sql内容
    env = models.CharField(max_length=6)  # 环境
    dbname = models.CharField(max_length=50)  # 目标数据库
    treater = models.CharField(max_length=20)  # 执行人
    status = models.IntegerField(default=-1, choices=SQL_STATUS)  # sql的执行状态
    executerz = models.CharField(max_length=200)  # sql执行的结果
    # exedatetime = models.CharField(max_length = 11)
    exe_affected_rows = models.CharField(max_length=10)  # 执行影响的行数
    roll_affected_rows = models.CharField(max_length=10)  # 回滚影响的行数
    rollbackopid = models.TextField(blank=True, null=True)  # 回滚的id
    rollbackdb = models.CharField(max_length=100)  # 回滚数据库


class dbconf(Basemodel):
    GENDER_CHOICES = (
                        ('1', u'生产'),
                        ('2', u'测试'),
    )
    user = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    host = models.CharField(max_length=16)
    port = models.CharField(max_length=5)
    env = models.CharField(max_length=1, blank=True, null=True, choices=GENDER_CHOICES)