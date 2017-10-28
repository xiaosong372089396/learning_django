#-*- coding:utf-8 -*-

from django.contrib import admin
from .models import Qcloud_record

class UserAdmin(admin.ModelAdmin):
    list_display = ('date', 'username', 'ip', 'active')

admin.site.register(Qcloud_record, UserAdmin)
