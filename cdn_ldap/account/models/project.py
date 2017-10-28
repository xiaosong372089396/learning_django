# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from account.mixins import NoDeleteModelMixin

__all__ = ['Project']


class Project(NoDeleteModelMixin):
    # 项目名称
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    # 备注
    comment = models.TextField(blank=True, verbose_name=_('Comment'))
    # 创建时间
    date_created = models.DateTimeField(auto_now_add=True, null=True,
                                        verbose_name=_('Date created'))
    created_by = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name
    __str__ = __unicode__

    def delete(self, using=None, keep_parents=False):
        # 删除方法 判断用户名是不是默认 如果不是清除用户并且删除
        if self.name != 'Default':
            self.users.clear()
            return super(Project, self).delete()
        return True

    class Meta:
        ordering = ['name']
        verbose_name_plural = "项目"
        verbose_name = "项目"

    @classmethod
    def initial(cls):
        # 初始化项目
        default_project = cls.objects.filter(name='Default')
        if not default_project:
            project = cls(name='Default', created_by='System', comment='Default user Project')
            project.save()
        else:
            project = default_project[0]
        return project
