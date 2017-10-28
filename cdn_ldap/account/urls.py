# -*- coding:utf-8 -*-



from django.conf.urls import url
from django.contrib import admin
from account import views
urlpatterns = [
    url(r'login/$', views.UserLoginView.as_view(), name="login"),
    url(r'logout/$', views.UserLogoutView.as_view(), name='logout'),
]
