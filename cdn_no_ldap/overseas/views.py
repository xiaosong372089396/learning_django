#-*- coding:utf-8 -*-

from django.shortcuts import render
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.shortcuts import render_to_response, HttpResponse
from django.views.generic import TemplateView,ListView,View
from django.contrib.auth.decorators import login_required
from django.contrib import auth
import traceback
import json
from ccmapp.ccm_api import Ccm
import time
import models
from remote_api import  remote
from overseas.tasks import remoteAsync

class Get_Cache(TemplateView):
    template_name = 'overseas/overseas.html'

    def get_context_data(self, **kwargs):
        try:
            context = super(Get_Cache,self).get_context_data(**kwargs)
            return context
        except Exception,e:
            print traceback.format_exc(),e


class  DeleCache(View):

    def  post(self, request, *args, **kwargs):
        #value = remote()
        value = True
        if value is True:
            val = remoteAsync.delay()
            print val,1111,type(val)
            date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            ip = request.META['REMOTE_ADDR']
            username = request.user.username
            models.overseas.objects.create(date=date, username=username, ip=ip)
            ok = True
            result = '海外热更缓存删除成功'
            return HttpResponse(json.dumps({ 'ok': ok, 'result': result }), content_type='application/json')

