# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ServersGroup, ServersModel, EmpLoyeeModel
from .models import AliyunTemplate, ServerConf


@admin.register(ServersGroup)
class ServersGroupAdmin(admin.ModelAdmin):
    model = ServersGroup
    verbose_name_plural = '分组列表'


@admin.register(ServersModel)
class ServersModelAdmin(admin.ModelAdmin):
    model = ServersModel
    verbose_name_plural = "服务器列表"
    list_display = ('instance_name', 'instanceid', 'status', 'server_from', 'cpu', 'memory', 'public_ip')
    list_display_link = ('name',)
    search_fields = ('instance_name', 'server_from')


@admin.register(EmpLoyeeModel)
class EmpLoyeeModelAdmin(admin.ModelAdmin):
    model = ServersModel
    verbose_name_plural = "员工资产信息列表"


@admin.register(AliyunTemplate)
class AliyunTemplateAdmin(admin.ModelAdmin):
    model = AliyunTemplate
    verbose_name_plural = '阿里云模板列表'
    list_display = ('zone_id', 'cpu', 'mem', 'image', 'bandwidth', 'root_disk')


@admin.register(ServerConf)
class ServerConfAdmin(admin.ModelAdmin):
    model = ServerConf
    verbose_name_plural = '服务器配置列表'
    list_display = ('server_type', 'info_type', 'key', 'value')
    search_fields = ('server_type', 'info_type')



# Re-register UserAdmin
admin.site.unregister(ServersGroup)
admin.site.register(ServersGroup, ServersGroupAdmin)
admin.site.unregister(ServersModel)
admin.site.register(ServersModel, ServersModelAdmin)
admin.site.unregister(EmpLoyeeModel)
admin.site.register(EmpLoyeeModel, EmpLoyeeModelAdmin)
