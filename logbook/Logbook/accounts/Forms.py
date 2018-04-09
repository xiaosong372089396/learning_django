# -*- coding:utf-8 -*-

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=24)
    password = forms.CharField(max_length=24)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.initial = self.initial or {'username': '', 'password': ''}
