#-*- coding:utf-8 -*-

from django.contrib import admin
from .models import txnetwork,Txpad

class Txaddress(admin.ModelAdmin):
    list_display = ('urlpad',)

admin.site.register(Txpad,Txaddress)

class Userinfo(admin.ModelAdmin):
    list_display = ('date', 'username', 'ip', 'flushurl', 'flushpath')

admin.site.register(txnetwork, Userinfo)