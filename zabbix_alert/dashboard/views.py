# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponse
import django.shortcuts
from django.contrib.auth.decorators import login_required
# from games.models import GameProject
import json


@login_required()
def index(request):
    if not request.user.is_authenticated():
        return django.shortcuts.redirect('/accounts/login')
    else:
        return django.shortcuts.redirect("/alertsapi/history_alert")
