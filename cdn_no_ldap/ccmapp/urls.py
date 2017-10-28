#-*- coding:utf-8 -*-

from django.conf.urls import include, url
from django.contrib.auth.decorators import  login_required
from ccmapp import views

urlpatterns = [
    url(r'get_ccmcdn/$',login_required(views.CcmCdn.as_view())),
    url(r'push/$', login_required(views.PushCcm.as_view()))
]