#-*- coding:utf-8 -*-

from django.contrib import admin
from .models import overseas

class UserAdmin(admin.ModelAdmin):
    list_display = ('date', 'username', 'ip')

admin.site.register(overseas, UserAdmin)


