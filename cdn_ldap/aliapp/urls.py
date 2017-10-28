#-*- coding:utf-8 -*-

from django.conf.urls import include, url
from django.contrib.auth.decorators import  login_required
from aliapp import views

urlpatterns = [
    url(r'get_alicdn/$',login_required(views.AliCdn.as_view())),
    url(r'push/$', login_required(views.PushValue.as_view()))
]