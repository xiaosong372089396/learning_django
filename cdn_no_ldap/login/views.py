#-*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')
from django.shortcuts import render,redirect
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.shortcuts import render_to_response
from django.views.generic import TemplateView,ListView,View
from django.contrib.auth.decorators import login_required
import traceback
from login.Forms import UserForm
#from login.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


"""
@login_required
def  index(request):
    return   render(request, 'cdn/index.html')

@login_required
def logouts(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def logins(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password = request.POST.get('password'))
        # user.is_active 用来判断用户名密码是否有效
        if user is not None and user.is_active:
            login(request,user)
            username = request.POST.get('username')
            return HttpResponseRedirect('/')
        else:
            login_error = "登陆失败,账号密码错误"
            return render(request, 'login/login.html', { 'login_error':login_error })
    return render(request, 'login/login.html')
"""
class index(LoginRequiredMixin, TemplateView):
    template_name = 'cdn/index.html'

    def get(self, request, *args, **kwargs):
        context = super(index, self).get_context_data(**kwargs)
        return self.render_to_response(context)



class userlogout(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('login'))


class userlogin(TemplateView):
    template_name = 'login/login.html'

    def get(self, request, *args, **kwargs):
        context = super(userlogin, self).get_context_data(**kwargs)
        context['request'] = self.request
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = super(userlogin, self).get_context_data(**kwargs)
        username = request.POST.get("username") or None
        password = request.POST.get("password") or None
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # print request.user.profile.privilege,1111
            login(request, user)
            username = request.POST.get('username')
            return HttpResponseRedirect('/')
        else:
            login_error = "登陆失败,账号密码错误"
            context["login_error"] = login_error
            return self.render_to_response(context)    
