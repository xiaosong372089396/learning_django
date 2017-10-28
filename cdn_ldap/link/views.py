#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "YaoYao"
# Date: 2017/8/6

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView
from link.models import Link
from django.forms.models import model_to_dict
from django.db.models import QuerySet
from account.models.user import User
# Create your views here.


class Index(TemplateView):

    template_name = 'link/index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['link'] = Link.objects.filter(groups__users__username=self.request.user)
        return context


