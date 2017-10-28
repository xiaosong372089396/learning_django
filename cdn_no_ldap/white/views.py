#-*- coding:utf-8 -*-

from django.shortcuts import render
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.shortcuts import render_to_response, HttpResponse
from django.views.generic import TemplateView,ListView,View
from django.contrib.auth.decorators import login_required
from django.contrib import auth
import traceback
import json
from white.White_api import  PushWhiteCdn
import time
import models

class WhiteCdn(TemplateView):
    template_name = 'white/whitecloud.html'

    def get_context_data(self, **kwargs):
        try:
            context = super(WhiteCdn,self).get_context_data(**kwargs)
            return context
        except Exception,e:
            print traceback.format_exc(),e

    def post(self,request, *args, **kwargs):
        pass

class  PushCdn(View):

    def post(self, request, *args, **kwargs):
        try:
            url = request.POST.getlist('fom','')
            data = PushWhiteCdn()
            value = data.Push(url)
            print value,11111111111111111
            if url:
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                ip = request.META['REMOTE_ADDR']
                username = request.user.username
                models.Whitecloud.objects.create(date=date, username=username, ip=ip, active=url)
                ok = True
                result = '提交成功'
                return HttpResponse(json.dumps({'ok': ok, 'result': result, 'data': value}),content_type='application/json')
            else:
                ok = False
                result = '提交失败'
                return HttpResponse(json.dumps({'ok': ok, 'result': result, 'data': value}),content_type='application/json')
        except Exception, e:
            print traceback.format_exc(), e


