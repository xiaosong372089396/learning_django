# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth.models import User
from dashboard.api.zabbix_api import tools
from django.http import HttpResponse, JsonResponse
from accounts.views import control_permission_context
import json
import paramiko


class Base(TemplateView):

    template_name = 'dashboard/base.html'
    def get_context_data(self, **kwargs):
        context = super(Base, self).get_context_data(**kwargs)
        return context



class GetHostdata(TemplateView):
    template_name = 'SHANXI/SHANXI.html'

    # @control_permission_context("*")
    def get_context_data(self, **kwargs):
        context = super(GetHostdata, self).get_context_data(*kwargs)
        data = tools()
        result = data.groupid_gethost(11)
        context['host'] = result
        return context

    def post(self, request, *args, **kwargs):
        context = {}
        return context

class Connectserver(View):

    def get(self,  request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass