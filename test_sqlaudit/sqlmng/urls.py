# -*- coding:UTF-8 -*-

from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^inception_commit/$', inception_commit.as_view()),
    url(r'^inception_result/(?P<pk>\d+)?/?(?P<actiontype>\w+)?$', inception_result.as_view(), name='inception_result'),
    url(r'^dbconfig/(?P<pk>\d+)?/?$', dbconfig.as_view(), name='dbconfig'),
    url(r'^autoselect/$', autoselect.as_view(), name='autoselect'),
]
