from django.conf.urls import include, url
from django.contrib.auth.decorators import  login_required
from alertsapi import views

urlpatterns = [
    url(r'history_alert/$',login_required(views.AlertsServer.as_view())),
    url(r'today_alert/$',login_required(views.TodayAlert.as_view())),
    url(r'contact_alert/$',login_required(views.ContactAlert.as_view())),
    url(r'api_deleuser/$', login_required(views.DeleUser.as_view()))
]

