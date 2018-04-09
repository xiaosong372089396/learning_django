# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import HttpResponse
import json
import traceback
from Forms import LoginForm



# 判断是否有访问的权限
def control_permission(subject):
    def _control(func):
        def __control(self, request):
            if str(subject) in self.request.user.permission:
                return func(self, self.request)
            else:
                raise Http404
        return __control
    return _control


# for get_context_data
# 控制权限上下文切换
def control_permission_context(subject):

    def _control(func):
        def __control(self, **kwarg):
            if str(subject) in self.request.user.permission:
                return func(self, **kwarg)
            else:
                raise Http404
        return __control
    return _control



class Login(TemplateView):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        context = super(Login, self).get_context_data(**kwargs)
        context['form'] = LoginForm()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('/')
            else:
                error_msg = '用户名或密码错误'
        else:
            error_msg = '用户名或密码不合法!'
        messages.info(request, error_msg)
        context = super(Login, self).get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('/account/login/')
