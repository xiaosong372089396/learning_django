#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "YaoYao"
# Date: 2017/8/2
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.
from account.models.group import UserGroup


class Link(models.Model):

    COLOR_CHOICES = (
        ('primary', _('primary')),
        ('warning', _('warning')),
        ('purple', _('purple')),
        ('dark', _('dark')),
        ('info', _('info')),
        ('success', _('success'))
    )
    name = models.CharField(max_length=256, verbose_name=_('链接名'))
    alias = models.CharField(max_length=128, verbose_name=_("别名"))
    groups = models.ManyToManyField(UserGroup, related_name=_("links"), verbose_name=_('所属组'))
    color = models.CharField(choices=COLOR_CHOICES, default="primary", max_length=24, verbose_name=_('颜色'))
    url = models.URLField(verbose_name=_('URl'))
    memo = models.CharField(max_length=128, verbose_name=_('备注'))

    def __unicode__(self):
        return self.name

    class Meta:

        ordering = ["name"]
