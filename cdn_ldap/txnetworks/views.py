#-*- coding:utf-8 -*-


from django.shortcuts import render
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.shortcuts import render_to_response, HttpResponse
from django.views.generic import TemplateView,ListView,View
from django.contrib.auth.decorators import login_required
from django.contrib import auth
import traceback
import json
import time
import models
from Tx_api import PushTxCdn


rest_prefix = "https://openapi.kr.cdnetworks.com/purge/rest/doPurge?"
user = ""
password = ""
output = "json"


class TxCdn(TemplateView):
    template_name = 'txwd/txwd.html'

    def get_context_data(self, **kwargs):
        try:
            context = super(TxCdn,self).get_context_data(**kwargs)
            urlpad = models.Txpad.objects.all()
            context['urlpad'] = urlpad
            return context
        except Exception,e:
            print traceback.format_exc(),e

    def post(self, request, *args, **kwargs):
        pass

class PushTx(View):

    def post(self, request):
        try:
            padurl = self.request.POST.getlist('options','')
            textarea = self.request.POST.getlist('textareas','')
            pad = str(padurl).strip('\\n').strip('[').strip(']').strip("u'").split('\\n')
            for pads in pad:
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                ip = request.META['REMOTE_ADDR']
                username = request.user.username
                models.txnetwork.objects.create(date=date, username=username, ip=ip, flushurl=pads, flushpath=textarea)
                data = PushTxCdn(rest_prefix, user, password, output, pads, user, textarea) #textarea
                value = eval(data.purage_data())
                if value['resultCode'] == 200:
                    data = pads + '' + str(value['paths']).strip('\\n').strip('[').strip(']').strip("u'") + ' ' +  ' '  + 'Cdn刷新成功，在10分钟内同步完成！'.encode('utf-8')
                    ok = True
                    result = '提交成功'
                    return HttpResponse(json.dumps({'ok': ok, 'result': result, 'data' : data }),content_type='application/json')
                elif value['resultCode'] == 400:
                    data = pads + '' + str(value['paths']) + ' ' + '接口请求无法完成，失败'.encode('utf-8')
                    ok = False
                    result = '提交失败'
                    return HttpResponse(json.dumps({'ok': ok, 'result': result, 'data': data}),content_type='application/json')
                elif value['resultCode'] == 403:
                    data = pads + '' + str(value['paths']) + ' ' + '登录失败'.encode('utf-8')
                    ok = False
                    result = '提交失败'
                    return HttpResponse(json.dumps({'ok': ok, 'result': result, 'data': data}),content_type='application/json')
                elif value['resultCode'] == 404:
                    data = pads + '' + str(value['paths']) + ' ' + '不正确接口调用'.encode('utf-8')
                    ok = False
                    result = '提交失败'
                    return HttpResponse(json.dumps({'ok': ok, 'result': result, 'data': data}),content_type='application/json')
                elif value['resultCode'] == 500:
                    data = pads + '' + str(value['paths']) + ' ' + '意外错误发生，请联系该项目运维！'.encode('utf-8')
                    ok = False
                    result = '提交失败'
                    return HttpResponse(json.dumps({'ok': ok, 'result': result, 'data': data}),content_type='application/json')
                elif value['resultCode'] == 509:
                    data = pads + '' + str(value['paths']) + ' ' + '超过API率限制！'.encode('utf-8')
                    ok = False
                    result = '提交失败'
                    return HttpResponse(json.dumps({'ok': ok, 'result': result, 'data': data}),content_type='application/json')
                else:
                    data = pads + '' + str(value['paths']) + ' ' + 'Cdn刷新失败，请联系该项目运维同学！'.encode('utf-8')
                    ok = False
                    result = '提交失败'
                    return  HttpResponse(json.dumps({'ok': ok, 'result': result, 'data': data }),content_type='application/json')
        except Exception, e:
            print traceback.format_exc(), e
