# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms


class AlertsForm(forms.Form):
    username = forms.CharField(required=True)
    mobile   = forms.CharField(max_length=11, required=True)

    def __init__(self, *args, **kwargs):
        super(AlertsForm, self).__init__(*args, **kwargs)
        self.initial = self.initial or {'username': '', 'mobile': ''}


class DeleUserProfile(forms.Form):
    id = forms.CharField(max_length=3)

    def __init__(self, *args, **kwargs):
        super(DeleUserProfile,self).__init__(*args,**kwargs)
        self.initial = self.initial or {'id':''}
