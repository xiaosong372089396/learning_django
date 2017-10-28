#-*- coding:utf-8 -*-

from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
#from login.models import  User
from django import forms
from django.forms import fields  #创建方法
from django.forms import widgets #方法属性值

#定义表单模型
class UserForm(forms.Form):
    username = forms.CharField(max_length=50,required="")
    password = forms.CharField(max_length=50, required="")

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args,**kwargs)
        self.initial = self.initial or {'username': '', 'password': ''}
