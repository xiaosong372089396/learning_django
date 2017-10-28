from django.contrib import admin

# Register your models here.

from zabbix import models



admin.site.register(models.Hosts)
admin.site.register(models.Groups)
admin.site.register(models.Triggers)
admin.site.register(models.Templates)
admin.site.register(models.Graphs)
admin.site.register(models.Items)
admin.site.register(models.Proxy)