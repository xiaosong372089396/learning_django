#-*- coding:utf-8 -*-

from django.conf.urls import include, url
from django.contrib.auth.decorators import  login_required
from white  import views

urlpatterns = [
    url(r'get_whitecdn/$',login_required(views.WhiteCdn.as_view())),
    url(r'push_white/$', login_required(views.PushCdn.as_view()))
]