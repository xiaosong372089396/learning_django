
from django.conf.urls import url,include
from django.contrib import admin
from dashboard import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.index,name='index'),
    url(r'^alertsapi/', include('alertsapi.urls')),
    url(r'^accounts/', include('accounts.urls')),
]