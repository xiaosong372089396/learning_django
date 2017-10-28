# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from account import forms
from django.contrib.auth import login as auth_login, logout as auth_logout,authenticate
from django.shortcuts import reverse, redirect, HttpResponseRedirect
from django.views.generic.base import View
from django.views.generic.edit import FormView
from utils import write_login_log
from account.models.user import User
from django.forms.models import model_to_dict
import json

# ldap 验证
# from login.ldap_auth_api import LdapApi
# from cdndir.settings import ldap_config

class UserLoginView(FormView):
    template_name = 'login/login.html'
    form_class = forms.UserLoginForm
# 表单验证 self.fields['service'] =
# form.CharField(widget=forms.HiddenInput,initial=service)
    redirect_field_name = '/account/login'  # index 请求验证失败访问
# 请求验证成功访问
    success_redirect = '/'        # /qcloud_cdn

    def get(self, request, *args, **kwargs):
        print "get"
        service = self.request.GET.get('service', None)  # 单点登陆URL地址,service参数值
        print "service is ", service
        print "self.request.user", self.request.user
        if self.request.user.is_authenticated():
            if service is not None:                     # server is None
                print "service is not None"
                if service.find('?') == -1:  # service not None 判断查找提交参数中?中参数, 是否等于-1
                    return redirect(service)  # 重定向到第一次提交访问地址,http://127.0.0.1:8000/service=
                else:
                    return redirect(service)
            else:
                print "service is None", service,111   # 输出GET,SERVICE 值,
                return redirect(self.get_success_url())  # 如果service not None 重定向下面函数处理
        if self.request.user.is_staff:           # 布尔值,指明这个用户是否可以进入管理站点, 都总是False
            return redirect(self.get_success_url())  # 重定向
        if 'form' not in kwargs:                 # 判断'form' not in kwargs
            kwargs['form'] = self.get_form(service=service)
        return super(UserLoginView, self).get(request, *args, **kwargs)  # 引用父类

    def get_form(self, service=None, form_class=None):
        if form_class is None:                   # form_class  is None
            form_class = self.get_form_class()   # None
        return form_class(service=service, **self.get_form_kwargs())  # 实例话类

    def form_valid(self, form):
        print "form_valid"
        login_ip = self.request.META.get('REMOTE_ADDR', None)   # 客户端IP,申请是经过代理服务器的话,那么它可能是以都好分割
        user_agent = self.request.META.get('HTTP_USER_AGENT', None)  # user浏览器user-agent字符串
        # You must get it in GET mode service
        service = self.request.GET.get("service", None)    # GET mode 获取
        # POST request 获取
        username = form.cleaned_data['username']           # 从login.html中获取username,password
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)   # local authenticate username, password

        # email = '%s' + '@' + 'ixianlai.com' % username
        # User.objects.get_or_create(username=username, password=password, name=username, email=email, created_by=username)
        # 判断用户是否在这个组中
        # result = user.is_member_of(user_group="安全运维部")
        # print result,2222
        # if not result:
        #    print 3333
        #    return redirect('index')


        if user is not None:        # user is not None
            print "user is not None"
            if user.is_active:           # 验证账户是否活动的,检验合法性
                print "user is active"
                auth_login(self.request, form.get_user())   # 获取请求用户登陆
                self.set_sso_user_info()
                write_login_log(self.request.user.username,    # 获取USER信息
                                self.request.user.name,        # 获取登陆用户名称
                                login_ip=login_ip,             # 获取客户端登陆IP
                                user_agent=user_agent)         # 获取客户端USER浏览器user-agent字符串
                if service is not None:                        # service is Not None
                    print "service is not None"
                    if service.find('?') == -1:                # 从service中查找? True,赋值-1
                        return redirect(service)               # 重定向到service
                    else:
                        return redirect(service)               # False,重定向service
                else:                                          # service is None
                    return redirect(self.get_success_url())    # 重定向到 get_success_url来处理
        return self.get_context_data()


    def get_success_url(self):
        if self.request.user.is_first_login:   # service is None 判断用户登陆,如果为True,反向解析到 index
            return reverse('index')            # 反向解析 index
        return self.request.POST.get(
            self.redirect_field_name,  # POST获取,redirect_field_name = 'index' 请求验证失败访问, 否则就获取GET请求反向解析
            self.request.GET.get(self.redirect_field_name, reverse('index')))
        # GET 请求redirect_field_name = 'index',反向解析 reverse('index')

    def set_sso_user_info(self):
        username = self.request.user   # 获取验证通过后用户

        print self.request.user.role   # 获取用户等级
        print "set_sso_user_info", username
        sso_user_info = User.objects.get(username=username).to_json()  # 从User库获取username用户,然后转为JSON格式
        self.request.session["sso_user_info"] = json.dumps(sso_user_info)  # 然后保存在session中, JSON格式转json.dumps转成字符串


class UserLogoutView(View):

    def get(self, request, *args, **kwargs):
        auth_logout(request)                  # 退出登陆
        return HttpResponseRedirect('/account/login')              # 重定向



