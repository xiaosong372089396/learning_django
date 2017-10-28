#-*- coding:utf-8 -*-

from django.shortcuts import render
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.shortcuts import render_to_response, HttpResponse
from django.views.generic import TemplateView,ListView,View
from django.contrib.auth.decorators import login_required
from django.contrib import auth
import traceback
import json
from alertsapi.models import Alerts
from alertsapi.models import Alert_User
from alertsapi.forms  import AlertsForm
from alertsapi.forms  import DeleUserProfile
from alertsapi.Daemon_Rabbit import QueueAPI
import time


class AlertsServer(TemplateView):
    template_name = 'alerts/index.html'

    def get_context_data(self, **kwargs):
        try:
            context = super(AlertsServer,self).get_context_data(**kwargs)
            context['all'] = Alerts.objects.all()
            # 导入Alerts表
            limit = 10  # 每页显示的记录数
            contact_list = Alerts.objects.all()
            # 设置默认显示页数, 每页默认记录3条
            paginator = Paginator(contact_list, limit)  # 实例化一个分页对象
            page = self.request.GET.get('page')  # 获取页码
            print page
            try:
                contacts = paginator.page(page)  # 获取页码对应记录
                print contacts
            except PageNotAnInteger:  # 如果页码不是整数
                contacts = paginator.page(1)  # 取第一页的记录
            except EmptyPage:  # 如果页码太大，每页相应的记录
                contacts = paginator.page(paginator.num_pages)  # 取最后一页的记录
            #邮件次数
            context['num'] = Alerts.objects.values('hostname').count()
            context['OK'] = Alerts.objects.filter(status=' OK').count()
            context['PROBLEM'] = Alerts.objects.filter(status=' PROBLEM').count()
            context['contacts'] = contacts
            return context
        except Exception,e:
            print traceback.format_exc(),e


class TodayAlert(TemplateView):
    template_name = 'alerts/today.html'

    def get_context_data(self, **kwargs):
        try:
            context = super(TodayAlert,self).get_context_data(**kwargs)
            localtime = time.strftime("%Y-%m-%d", time.localtime())
            context['today_all'] = Alerts.objects.filter(times__contains='2017-02-25')
            # 导入Alerts表
            limit = 10  # 每页显示的记录数
            contact_list = Alerts.objects.filter(times__contains=localtime)
            # 设置默认显示页数, 每页默认记录3条
            paginator = Paginator(contact_list, limit)  # 实例化一个分页对象
            page = self.request.GET.get('page')  # 获取页码
            #print page
            try:
                contacts = paginator.page(page)  # 获取页码对应记录
                #print contacts
            except PageNotAnInteger:  # 如果页码不是整数
                contacts = paginator.page(1)  # 取第一页的记录
            except EmptyPage:  # 如果页码太大，每页相应的记录
                contacts = paginator.page(paginator.num_pages)  # 取最后一页的记录
            context['contacts'] = contacts
            context['OK'] = Alerts.objects.filter(times__contains=localtime,status=' OK').count()
            context['PROBLEM'] = Alerts.objects.filter(times__contains=localtime, status=' PROBLEM').count()
            values = Alerts.objects.filter(times__contains=localtime).values('hostname','message','status','level','times')
            # http://www.yihaomen.com/article/python/526.htm
            print values
            context['num'] = Alerts.objects.filter(times__contains=localtime).count()
            return  context
        except Exception, e:
            print traceback.format_exc(),e


class ContactAlert(TemplateView):
    template_name = 'alerts/contact.html'

    def get_context_data(self, **kwargs):
        context = super(ContactAlert,self).get_context_data(**kwargs)
        # 导入Alerts表
        limit = 10  # 每页显示的记录数
        contact_list = Alert_User.objects.all()
        # 设置默认显示页数, 每页默认记录3条
        paginator = Paginator(contact_list, limit)  # 实例化一个分页对象
        page = self.request.GET.get('page')  # 获取页码
        try:
            contacts = paginator.page(page)  # 获取页码对应记录
            # print contacts
        except PageNotAnInteger:  # 如果页码不是整数
            contacts = paginator.page(1)  # 取第一页的记录
        except EmptyPage:  # 如果页码太大，每页相应的记录
            contacts = paginator.page(paginator.num_pages)  # 取最后一页的记录
        context['formss'] = DeleUserProfile
        context['contacts'] = contacts
        return context

    def post(self, request, *args, **kwargs):
        try:
            username = self.request.POST.get('username','')
            mobile   = self.request.POST.get('mobile','')
            task = Alert_User.objects.get_or_create(username=username, mobile=mobile)
            #新建时返回True, 已经存在时返回False
            if task:
                ok = True
                result = '添加成功'
                return HttpResponse(json.dumps({'ok': ok, 'result': result}), content_type='application/json')
            else:
                ok = False
                result = '添加失败'
                return HttpResponse(json.dumps({'ok': ok, 'result': result}), content_type='application/json')
        except Exception, e:
            print traceback.format_exc(), e


class  DeleUser(View):

    def post(self, request, *args, **kwargs):
        try:
            form = DeleUserProfile(request.POST)
            if form.is_valid():
                id = form.cleaned_data['id']
                task = Alert_User.objects.filter(id=id).delete()
                if task:
                    ok = True
                    result = '删除成功'
                    return HttpResponse(json.dumps({'ok': ok, 'result': result}), content_type='application/json')
                else:
                    ok = False
                    result = '删除失败'
                    return HttpResponse(json.dumps({'ok': ok, 'result': result}), content_type='application/json')
        except Exception,e:
            print traceback.format_exc(),e
