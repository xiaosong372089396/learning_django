# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import GroupManager
from django.utils.translation import ugettext_lazy as _

__all__ = ['UserGroup']


class UserGroup(models.Model):
    name = models.CharField(max_length=128, verbose_name='部门名')
    # 部门
    comment = models.TextField(blank=True, verbose_name=_('Comment'))
    # 创建时间
    date_created = models.DateTimeField(auto_now_add=True, null=True,
                                        verbose_name=_('Date created'))
    created_by = models.CharField(max_length=100)

    objects = GroupManager()

    def __unicode__(self):
        return self.name
    __str__ = __unicode__

    def delete(self, using=None, keep_parents=False):
        # 删除方法 判断用户名是不是默认 如果不是清除用户并且删除
        if self.name != '闲徕互娱':
            self.users.clear()
            return super(UserGroup, self).delete()
        return True

    @classmethod
    def initial(cls):
        # 初始化部门
        default_group = cls.objects.filter(name='闲徕互娱')
        if not default_group:
            group = cls(name='闲徕互娱', created_by='Default', comment='Default user Department')
            group.save()
        else:
            group = default_group[0]
        return group

    class Meta:
        ordering = ['name']
        verbose_name = "部门"
        verbose_name_plural = "部门"

    def __unicode__(self):
        return self.name
