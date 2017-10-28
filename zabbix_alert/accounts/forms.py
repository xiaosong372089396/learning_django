# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from accounts import models
from django.forms import ModelForm
import traceback


class ProfileForm(ModelForm):
    class Meta:
        model = models.Profile  # 关联的表
        exclude = ()

    def __new__(cls, *args, **kwargs):
        for field_name in cls.base_fields:
            field = cls.base_fields[field_name]
            attr_dic = {'class': 'form-control',
                            'placeholder': field.help_text,
                           }
            field.widget.attrs.update(attr_dic)
        return ModelForm.__new__(cls)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=24)
    password = forms.CharField(max_length=24)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.initial = self.initial or {'username': '', 'password': ''}


class ChangePasswordForm(forms.Form):
    password_current = forms.CharField(max_length=24)
    password_new = forms.CharField(max_length=24)
    password_new_confirm = forms.CharField(max_length=24)

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.initial = self.initial or {'password_current': '', 'password_new': '', 'password_new_confirm': ''}

    def clean_password_current(self):
        if not self.user.check_password(self.cleaned_data.get('password_current')):
            raise forms.ValidationError(u'原始密码错误')
        return self.cleaned_data['password_current']

    def clean_password_new_confirm(self):
        if 'password_new' in self.cleaned_data and 'password_new_confirm' in self.cleaned_data:
            if self.cleaned_data['password_new'] != self.cleaned_data['password_new_confirm']:
                raise forms.ValidationError(u'两次新密码不一致！')
        return self.cleaned_data['password_new_confirm']


def get_profile(query_key, query_value):
    results = models.Profile.objects.filter()
    query_item = ['全部', ]
    try:
        if query_key and query_key != '全部':
            query_item = [query_key, ] + query_item
            results = results.filter(department__name=query_key)
        if query_value:
            results = results.filter(name__contains=query_value)
    except Exception, e:
        print traceback.format_exc()

    departments = models.Department.objects.all()
    for one in departments:
        query_item.append(one.name)

    return results, query_item

