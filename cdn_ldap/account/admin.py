# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import Group
from account.models.user import User
from account.models.project import Project
from account.models.logs import LoginLog
from account.models.group import UserGroup
admin.site.register(User)
admin.site.register(UserGroup)


class LoginLogAdmin(admin.ModelAdmin):
    list_display = ("username", "login_ip", "login_city", "user_agent", "date_login")

admin.site.register(LoginLog, LoginLogAdmin)
admin.site.register(Project)
admin.site.unregister(Group)
