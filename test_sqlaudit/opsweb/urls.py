# -*- coding:UTF-8 -*-

"""opsweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^favicon.ico$', RedirectView.as_view(url=r'static/images/favicon.ico')), 
    url(r'^admin/', admin.site.urls),
    url(r'^$', login_required(TemplateView.as_view(template_name="index.html"))),

    #  django Exception Value:	 'tuple' object is not callable 报错缺少页面里面函数变量
    url(r'^indextest/$', TemplateView.as_view(template_name="indextest.html")),
    url(r'^sqlmng/', include('sqlmng.urls')),
    url(r'^accounts/', include('accounts.urls')),


]

