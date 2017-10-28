#-*-coding:utf-8-*-
from django.conf.urls import url,include
from django.contrib.auth.decorators import login_required
from zabbix import views

urlpatterns = [
    url(r'^index/$', views.Index.as_view(), name='index'),
    url(r'^host/$', views.Hostlist.as_view(), name='host'),
    url(r'^group/$', views.Grouplist.as_view(), name='group'),
    url(r'^template/$', views.Templateist.as_view(), name='template'),
    url(r'^createhost/$', views.CreateHost.as_view(), name='createhost'),
    url(r'^creategroup/$', views.CreateGroup.as_view(), name='creategroup'),
    url(r'^item/$', views.ItemLlist.as_view(), name='itemlist'),
    url(r'^graph/$', views.Graphlist.as_view(), name='graphlist'),
    url(r'^trigger/$', views.Triggerlist.as_view(), name='triggerlist'),
    url(r'^history/$', views.Historylist.as_view(), name='historylist'),
]
