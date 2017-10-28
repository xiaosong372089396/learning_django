#-*- coding:utf-8 -*-

from django.conf.urls import include, url
from django.contrib.auth.decorators import  login_required
from txnetworks import views

urlpatterns = [
    url(r'get_txwdcdn/$',login_required(views.TxCdn.as_view())),
    url(r'pushtxwd/$', login_required(views.PushTx.as_view()))
]