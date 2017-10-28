# -*- coding: utf-8 -*-



from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django import forms
from account import models
from django.forms import ModelForm


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label=_('Username'), max_length=100)
    password = forms.CharField(
        label=_('Password'), widget=forms.PasswordInput, max_length=100,
        strip=False)

    def __init__(self, service=None, request=None, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.request = request
        if service is not None:
            print "form service is not None"
            self.fields['service'] = forms.CharField(widget=forms.HiddenInput, initial=service)  # 隐藏
