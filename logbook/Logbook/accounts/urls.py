# -*- coding:utf-8 -*-

from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from views import Login, logout_view


urlpatterns = [
    url(r'^login/$',  Login.as_view(), name='login'),
    url(r'^logout/$', logout_view, name='logout'),
]