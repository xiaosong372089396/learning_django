# -*- coding:utf-8 -*-

from django.contrib import admin
from models import User_Permission


class UserAdmin(admin.ModelAdmin):
    model = User_Permission
    verbose_name_plural = '用户列表'
    list_display = ('name', 'level', 'permission')
    list_display_links = ('name',)


admin.site.register(User_Permission, UserAdmin)



