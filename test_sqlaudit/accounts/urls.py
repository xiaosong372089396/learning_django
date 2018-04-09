# -*- coding:UTF-8 -*-

from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^login/', Login_View.as_view(), name='login'),
    url(r'^logout/', Logout_View.as_view(), name='logout'),
]
