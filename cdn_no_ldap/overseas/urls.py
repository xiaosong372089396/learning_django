#-*- coding:utf-8 -*-

from django.conf.urls import include, url
from django.contrib.auth.decorators import  login_required
from overseas import views

urlpatterns = [
    url(r'get_cache/$',login_required(views.Get_Cache.as_view())),
    url(r'dete_cache/$', login_required(views.DeleCache.as_view()))
]
