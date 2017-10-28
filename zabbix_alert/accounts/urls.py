# Create your models here.
# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import LoginView, logout_view
from django.contrib.auth.decorators import login_required
from accounts import views

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout_view, name='logout'),
]
