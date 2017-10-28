# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
from collections import OrderedDict
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.core import signing
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.shortcuts import reverse
from account.tools import date_expired_default
from account.models.project import Project
from account.models.group import UserGroup
__all__ = ['User']


class User(AbstractUser):

    ROLE_CHOICES = (
        ('Admin', _('Administrator')),
        ('User', _('User')),
        ('App', _('Application')),
        ('Proj', _('Project'))
    )
    username = models.CharField(max_length=20, unique=True, verbose_name=_('Username'))
    name = models.CharField(max_length=20, verbose_name=_('Name'))
    email = models.EmailField(max_length=30, verbose_name=_('Email'))
    groups = models.ManyToManyField(UserGroup, related_name='users', null=True,
                                    blank=True, verbose_name=_('User group'))
    project = models.ManyToManyField(Project, verbose_name=_("Project"),
                                     null=True, blank=True)
    role = models.CharField(choices=ROLE_CHOICES, default='User', max_length=10,
                            blank=True, verbose_name=_('Role'))
    avatar = models.ImageField(upload_to="avatar", null=True, verbose_name=_('Avatar'))
    wechat = models.CharField(max_length=30, blank=True, verbose_name=_('Wechat'))
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Phone'))
    enable_otp = models.BooleanField(default=False, verbose_name=_('Enable OTP'))
    comment = models.TextField(max_length=200, blank=True, verbose_name=_('Comment'))
    is_first_login = models.BooleanField(default=False)
    date_expired = models.DateTimeField(default=date_expired_default, blank=True, null=True,)
    created_by = models.CharField(max_length=30, default='', verbose_name=_('Created by'))

    # 将类方法转换为只读属性
    # 当将类方法转换为只读属性之后 不能将该属性设为其他值

    @property
    def password_raw(self):
        raise AttributeError('Password raw is not a readable attribute')

    #: Use this attr to set user object password, example
    #: user = User(username='example', password_raw='password', ...)
    #: It's equal:
    #: user = User(username='example', ...)
    #: user.set_password('password')
    # 为password_raw属性创建一个setter方法
    @password_raw.setter
    def password_raw(self, password_raw_):
        # 设置密码
        self.set_password(password_raw_)

    @property
    def is_expired(self):
        # 验证失效时间
        if self.date_expired < timezone.now():
            return True
        else:
            return False

    @property
    def is_valid(self):
        # 验证是否激活和失效
        if self.is_active and not self.is_expired:
            return True
        return False

    @property
    def is_superuser(self):
        # 判断是否为管理员
        if self.role == 'Admin':
            return True
        else:
            return False

    @is_superuser.setter
    def is_superuser(self, value):

        # 设置用户为管理员
        if value is True:
            self.role = 'Admin'
        else:
            self.role = 'User'

    @property
    def is_app(self):
        # 设置用户为app用户
        return self.role == 'App'

    @property
    def is_proj(self):
        # 设置用户为Project用户
        return self.role == 'Proj'

    @property
    def is_staff(self):

        # 验证是否有权限和激活等等
        if self.is_authenticated and self.is_valid:
            return True
        else:
            return False

    @is_staff.setter
    def is_staff(self, value):
        pass

    def save(self, *args, **kwargs):
        # 判断有没有用户，如果没有 保存
        if not self.name:
            self.name = self.username

        super(User, self).save(*args, **kwargs)
        # Add the current user to the default group.
        # 添加到默认到group里
        if not self.project.count():
            project = Project.initial()
            self.project.add(project)

    def is_member_of(self, user_group):
        # 判断用户组在不在组里
        if user_group in self.groups.all():
            return True
        return False

    def avatar_url(self):
        # 返回头像地址
        if self.avatar:
            return self.avatar.url
        else:
            avatar_dir = os.path.join(settings.MEDIA_ROOT, 'avatar')
            if os.path.isdir(avatar_dir):
                return os.path.join(settings.MEDIA_URL, 'avatar', 'default.png')
        return 'https://www.gravatar.com/avatar/c6812ab450230979465d7bf288eadce2a?s=120&d=identicon'

    def to_json(self):
        # 将用户数据转换为json
        return OrderedDict({
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'is_active': self.is_active,
            'is_superuser': self.is_superuser,
            'role': self.get_role_display(),
            'groups': [group.name for group in self.groups.all()],
            'wechat': self.wechat,
            'phone': self.phone,
            'comment': self.comment,
            'date_expired': self.date_expired.strftime('%Y-%m-%d %H:%M:%S')
        })

    def reset_password(self, new_password):
        # 重置密码
        self.set_password(new_password)
        self.save()

    def delete(self):
        # 删除用户
        if self.pk == 1 or self.username == 'admin':
            return
        return super(User, self).delete()

    class Meta:
        # 根据用户名进行排序
        ordering = ['username']
        verbose_name = "用户"
        verbose_name_plural = "用户"

    @classmethod
    def initial(cls):
        # 初始化用户信息 默认创建admin用户
        user = cls(username='admin',
                   email='free@ixianlai.com',
                   name=_('Administrator'),
                   password_raw='admin',
                   role='Admin',
                   comment=_('Administrator is the super user of system'),
                   created_by=_('System'))
        user.save()
        # 添加用户组  用户组为初始化创建默认用户组
        user.groups.add(UserGroup.initial())



