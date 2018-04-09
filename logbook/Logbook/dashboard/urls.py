# -*- coding:utf-8 -*-

from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from views import GetHostdata


urlpatterns = [
    url(r'^shanxi/$',  GetHostdata.as_view(), name='shanxidata'),
]