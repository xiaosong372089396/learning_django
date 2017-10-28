#-*- coding:utf-8 -*-

from django.contrib import admin
from .models import CCMrecord

class UserAdmin(admin.ModelAdmin):
    list_display = ('date', 'username', 'ip', 'active')

admin.site.register(CCMrecord, UserAdmin)


