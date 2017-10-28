"""cdndir URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url,include
from django.contrib import admin
from login.views import index #logins
from submits.views import cdnrefresh ,index
from login import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    #   url(r'^login/$', views.logins),
    #   url(r'^logout/$', views.logouts),
    url(r'^qcloud_cdn/', index),
    url(r'cdnrefresh/', cdnrefresh),
    url(r'^alicloud/',  include('aliapp.urls')),
    url(r'^ccmcloud/',  include('ccmapp.urls')),
    url(r'^whitecloud/',include('white.urls')),
    url(r'^txwdcloud/', include('txnetworks.urls')),
    url(r'^overseas/', include('overseas.urls')),

    url(r'^account/', include('account.urls')),

]
