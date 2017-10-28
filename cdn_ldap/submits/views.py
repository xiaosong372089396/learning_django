#-*- coding:utf-8 -*-

import sys,os
reload(sys)
sys.setdefaultencoding('utf8')
from django.shortcuts import render
from cdn_api import Sign
from django.http import HttpResponse
import json
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.shortcuts import render_to_response
from django.views.generic import TemplateView,ListView,View
from django.contrib.auth.decorators import login_required
from django.contrib import auth
import traceback
import json
from login.Forms import UserForm
from cdn_api import secretId,secretKey
import traceback
import time
import models

@login_required
def index(request):
    return  render(request, 'cdn/qcloud.html')

@login_required
def  cdnrefresh(request):
    if request.method == 'POST':
        try:
            task = request.POST.getlist('fom','')
            #task 是一个list
            cdnDIRrefresh = Sign(secretId, secretKey)
            value = cdnDIRrefresh.cdnrefresh(task)
            timess = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
            print timess, value
            if task:
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                ip = request.META['REMOTE_ADDR']
                username = request.user.username
                models.Qcloud_record.objects.create(date=date, username=username, ip=ip, active=task)
                ok = True
                result = '提交成功'
                return HttpResponse(json.dumps({'ok': ok, 'result': result, 'data': value }), content_type='application/json')
            else:
                ok = False
                result = '提交失败'
                return HttpResponse(json.dumps({'ok': ok, 'result': result, 'data': value }), content_type='application/json')
        except Exception, e:
            print traceback.format_exc(), e
