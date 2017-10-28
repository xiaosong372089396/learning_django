# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, View
from django.contrib import messages
from models import Profile, Department, Role
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import datetime
import traceback
import json
import logging
import random
from .forms import LoginForm, ChangePasswordForm,ProfileForm, get_profile

logger = logging.getLogger("free")
PER_PAGE_NUM = 10

class LoginView(TemplateView):
    template_name = 'accounts/login.html'

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get(self, request, *args, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['form'] = LoginForm()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)  # 认证
            try:
                if user is not None and user.is_active:
                    profile = Profile.objects.get(user=user)
                    profile.last_login = datetime.datetime.utcnow()
                    profile.is_login = True
                    profile.save()
                    login(request, user)
                    #user_ip = self.get_client_ip(request)
                   # OperationModel.objects.create(pro=profile, ip=user_ip, user_name=profile.name, opt_type='日常行为', opt_content='登录')
                    # 返回登录前的页面
                    history_path = self.request.META.get('HTTP_REFERER', '/')
                    if 'accounts/login' in history_path:
                        history_path = history_path.split('next=')
                        if len(history_path) > 1:
                            history_path = history_path[1]
                            return redirect(history_path)
                        else:
                            return redirect('/')
                else:
                    error_msg = '用户名或密码错误！'
            except Exception, e:
                print traceback.format_exc()

        else:
            error_msg = serialize_form_errors(form)
            messages.info(request,error_msg)
        context = super(LoginView, self).get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)












@login_required
def logout_view(request):
    profile = Profile.objects.get(user=request.user)
    profile.is_login = False
    profile.save()
    if request.user.is_authenticated():
        OperationModel.objects.create(pro=profile, user_name=profile.name, opt_type='日常行为', opt_content='退出')
        logout(request)
    return redirect('/accounts/login/')


def serialize_form_errors(form):
    errors = []
    for field in form:
        if field.errors:
            errors.append(field.label + ':' + ','.join([err for err in field.errors]))
    return '\n'.join(errors)


class SetProfile(TemplateView):
    template_name = 'accounts/set_profile.html'
    def get_context_data(self, **kwargs):
        context = super(SetProfile, self).get_context_data(**kwargs)
        profile = self.request.user.profile
        context['profile'] = profile
        return context


def update_password(request):
    password = request.POST.get('password', '')
    password1 = request.POST.get('new_password', '')
    password2 = request.POST.get('new_password1', '')
    print password, password2, password1
    try:
        if request.user.check_password(password):
            user = User.objects.get(username=request.user.username)
            user.set_password(password1)
            user.save()
            return HttpResponse(json.dumps('修改成功'), content_type='application/json')
        else:
            return HttpResponse(json.dumps('失败,原密码错误'), content_type='application/json')
    except Exception, e:
        print traceback.format_exc()    
    return HttpResponse(json.dumps('失败,这个未知的错误需要伟大的管理员来解决'), content_type='application/json')


def update_head(request):
    file = request.FILES.get('file', '')
    if file:
        user = request.user.profile
        user.head_img.save(file.name, file)
        return redirect('/accounts/set_profile/')
    else:
        return redirect('accounts/set_profile/')


def send_cell_check(request):
    cell = request.POST.get('cell', '')
    num = str(random.randint(100000, 999999))
    user = request.user.profile
    user.memo = num
    user.save()
    content = "您好,您正在修改CMDB帐号的手机号,验证码: " + num
    re = Message(cell, content)
    return HttpResponse(json.dumps('发送成功'), content_type='application/json')


def update_cell(request):
    cell = request.POST.get('cell', '')
    check_num = request.POST.get('num', '')
    user = request.user.profile
    if user.memo == check_num:
        user.cell = cell
        user.memo = ''
        user.save()
        return HttpResponse(json.dumps('修改成功'), content_type='application/json')
    else:
        return HttpResponse(json.dumps('失败,验证码错误'), content_type='application/json')


class Register(TemplateView):
    """通过邮箱注册"""
    template_name = "accounts/register.html"
    def get_context_data(self, **kwargs):
        context = super(ServerList, self).get_context_data(**kwargs)
        return context

    def post(self, request):
        return redirect()


class CreateUser(View):
    '''get 方法是获取验证码的,post方法是创建用户的'''
    def get(self, request):
        try:
            mail = request.GET.get('mail', '')
            num = str(random.randint(100000, 999999))
            if mail.endswith("@ixianlai.com"):
                is_exist = Profile.objects.filter(mail=mail)
                if is_exist:
                    return HttpResponse(json.dumps({'info': "失败,该邮箱已注册"}),content_type="application/json")
                send_mail(mail, '闲徕互娱验证码', '您的闲徕互娱自动化运维平台验证码为: ' + num)
                return HttpResponse(json.dumps({'info': '验证码三分钟内有效', 'verify_num': num}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'info': "失败,只有闲徕互娱的邮箱才能注册"}),content_type="application/json")
        except Exception as e:
            logger.error(traceback.format_exc())


    def post(self, request):
        try:
            ver_num = request.POST.get('ver_num', '')
            mail = request.POST.get('mail', '')
            name = request.POST.get('name', '')
            password = random.choice("qwertupasdfghjklzcvbnm123456789") + str(random.randint(100000, 999999))
            login_name, _ = mail.split('@')
            user = User.objects.create_user(login_name, '', password)
            role = Role.objects.get(pk=1) # 默认普通人员
            department = Department.objects.get(pk=1) # 默认运维人员吧
            profile = Profile.objects.create(user=user, name=name, mail=mail, cell='0', role=role, department=department, head_img='static/userimg/default.png')
            profile.save()
            content = name + "您好,欢迎注册闲徕互娱自动化运维平台,您得帐号是: " + login_name + ", 密码是: " + password
            send_mail(mail, '闲徕互娱自动化运维平台帐号', content)
            return HttpResponse(json.dumps('帐号密码已发总至您邮箱,请查收'), content_type='application/json')
        except Exception as e:
            print traceback.format_exc()
