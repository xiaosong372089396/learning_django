#-*- coding:utf-8 -*-

from django.contrib import admin
from .models import Ali_record

class UserAdmin(admin.ModelAdmin):
    list_display = ('date', 'username', 'ip', 'active')

admin.site.register(Ali_record, UserAdmin)
