# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# from django.contrib.contenttypes import generic


class Role(models.Model):
    name = models.CharField(max_length=32, verbose_name='名称')
    alias = models.CharField(max_length=32, verbose_name='别名')

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = '角色列表'
        ordering = ['id']

    def __unicode__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=32, verbose_name='部门名')
    leader = models.ForeignKey(User, blank=True, null=True, verbose_name='部门领导')

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门列表'
        ordering = ['id']

    def __unicode__(self):
        return self.name


class Profile(models.Model):
    PRIVILEGE_CHOICES = (
        (1, '普通'),
        (2, '中级'),
        (3, '高级'),
        (4, '超级'),
    )

    ROLE_TYPE = (
        (1, '普通人员'),
        (2, '运维人员'),
        (3, '管理人员'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30,verbose_name="姓名")
    role = models.ForeignKey(Role, verbose_name='角色')
    role_type = models.IntegerField(choices=ROLE_TYPE, default=1, verbose_name="权限类型")
    head_img = models.ImageField(blank=True,null=True,verbose_name="头像", upload_to="static/userimg")
    privilege = models.IntegerField(choices=PRIVILEGE_CHOICES, default=1, verbose_name='权限')
    is_login = models.BooleanField(default=False, verbose_name='是否登录')
    last_login = models.DateTimeField(auto_now=True)
    department = models.ForeignKey(Department)
    mail = models.CharField(max_length=80, verbose_name='邮箱')
    cell = models.CharField(max_length=20, verbose_name='手机号')
    send_alarm = models.BooleanField(default=False, verbose_name="是否发送报警")
    memo = models.CharField(max_length=200, blank=True, null=True, verbose_name="备注")

    modify_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '附加用户信息'
        verbose_name_plural = '附加用户信息列表'
        ordering = ['id']

    def __unicode__(self):
        return 'the extra profile of %s' % self.user.get_full_name()
