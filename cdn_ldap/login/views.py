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
# Create your views here.

from django.core.urlresolvers import reverse
from account import forms


#@login_required
#def index(request):
#        return render(request, 'cdn/index.html')


@login_required
def index(request):
    return render(request, 'cdn/index.html')



@login_required
def logouts(request):
    logout(request)
    return HttpResponseRedirect('/login/')
'''
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
            return render(request, 'login/login.html', {'login_error': login_error})
    return render(request, 'login/login.html')


       if request.user.role != "Admin":
       pass
   if not request.user.is_authenticated():
       return redirect('/account/login')
   else:


'''

