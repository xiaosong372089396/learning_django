#-*- coding:utf-8 -*-

from django.contrib import admin
from .models import Alerts

@admin.register(Alerts)
class AlertsServer(admin.ModelAdmin):
    model = Alerts
    verbose_name_plural = '告警信息'

# Re-register UserAdmin
admin.site.unregister(Alerts)
admin.site.register(Alerts, AlertsServer)



