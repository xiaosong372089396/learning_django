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


class CcmCdn(TemplateView):
    template_name = 'ccm/ccmcloud.html'

    def get_context_data(self, **kwargs):
        try:
            context = super(CcmCdn,self).get_context_data(**kwargs)
            return context
        except Exception,e:
            print traceback.format_exc(),e

    def post(self, request, *args, **kwargs):
        pass

class PushCcm(View):

    def post(self, request, *args, **kwargs):
        try:
            url = self.request.POST.getlist('fom','')
            data = Ccm()
            value = data.ComBination(url)
            if url:
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                ip = request.META['REMOTE_ADDR']
                username = request.user.username
                models.CCMrecord.objects.create(date=date, username=username, ip=ip, active=url)

                ok = True
                result = '提交成功'
                return HttpResponse(json.dumps({'ok': ok, 'result': result, 'data': value }),content_type='application/json')
            else:
                ok = False
                result = '提交失败'
                return HttpResponse(json.dumps({'ok': ok, 'result': result, 'data': value }),content_type='application/json')
        except Exception, e:
            print traceback.format_exc(), e