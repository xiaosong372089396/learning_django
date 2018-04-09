# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')


import os
from collections import OrderedDict
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core import signing
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from tools import date_expired_default
from django.contrib.auth.models import User
from django.db import models



class User_Permission(models.Model):

    ROLE_CHOICES = (
        ('Admin', _('Administrator')),
        ('User', _('User')),
        ('App',  _('Application')),
        ('Proj', _('Project'))
    )
    LEVEL_CHOICES = (
        (1, _('超级管理员')),
        (2, _('高级管理员')),
        (3, _('中级管理员')),
        (4, _('初级管理员'))
    )
    name = models.ForeignKey(User, verbose_name="用户权限")
    # username = models.CharField(max_length=20, unique=True, verbose_name=_('Username'))
    # name = models.CharField(max_length=20, verbose_name=_('Name'))
    email = models.EmailField(max_length=30, verbose_name=_('Email'))
    role = models.CharField(choices=ROLE_CHOICES, default='User', max_length=10,
                            blank=True, verbose_name=_('Role'))
    level = models.IntegerField(choices=LEVEL_CHOICES, default=4, blank=True, verbose_name=_('级别'))
    avatar = models.ImageField(upload_to="avatar", null=True, blank=True, verbose_name=_('Avatar'))
    wechat = models.CharField(max_length=30, blank=True, verbose_name=_('Wechat'))
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Phone'))
    enable_otp = models.BooleanField(default=False, verbose_name=_('Enable OTP'))
    comment = models.TextField(max_length=200, blank=True, verbose_name=_('Comment'))
    is_first_login = models.BooleanField(default=False)
    date_expired = models.DateTimeField(default=date_expired_default, blank=True, null=True,)
    created_by = models.CharField(max_length=30, null=True, blank=True, verbose_name=_('Created by'))
    memo = models.CharField(max_length=256, blank=True, null=True, verbose_name=_('备注'))
    permission = models.CharField(max_length=200, blank=True, null=True, verbose_name="权限", help_text='z:安全权限(宋锦程), q:上海麻将, w:东北项目, e:云南麻将, r:四川麻将, t:天津麻将, y:宁夏麻将, u:山西麻将, i:广东,\
        o:掌上扑克, p:新湖南麻将, a:新疆麻将, s:江苏麻将, d:江西麻将, f:河南麻将, g:湖南麻将, h:福建麻将, j:胶己人麻将, k:腾讯内蒙古麻将, \
         l:腾讯安徽麻将, x:腾讯山东麻将, c:腾讯广西麻将, v:腾讯河北麻将, b:腾讯浙江, n:腾讯海南麻将, m:腾讯甘肃麻将, 1:西藏麻将, 2:贵州麻将, 3:赣州麻将, 4:跑得快, 5:跑胡子, 6:郴州跑胡子, 7:榆林麻将, 8:斗地主, 9:陕西麻将')
    create_time = models.DateTimeField(auto_now_add=True)
    # 将类方法转换为只读属性
    # 当将类方法转换为只读属性之后 不能将该属性设为其他值

    class Meta:
        db_table = "User_Permission"
        ordering = ['name']
        verbose_name = "权限管理"
        verbose_name_plural = "权限管理"


