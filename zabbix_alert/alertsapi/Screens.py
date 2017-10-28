#-*- coding:utf-8 -*-


from alertsapi.models import Alerts
from alertsapi import models


#短信收敛聚合：
def  HostName(times=None):
    ###主机名
    host_lists = list()
    host_object = Alerts.objects.filter(times__contains=times).values('hostname')    #### or  values('hostname')
    for i in host_object:
        for values in i.values():
            if values not in host_lists:
                host_lists.append(values)
    return host_lists

def  Message(times=None):
    ###告警信息
    message_lists = list()
    message_object = Alerts.objects.filter(times__contains=times).values('message')
    for i in message_object:
        for values in i.values():
            if values not in message_lists:
                message_lists.append(values)
    return  message_lists

def Status(times=None):
    ###当前状态
    status_lists = list()
    status_object = Alerts.objects.filter(times__contains=times).values('status')
    for i in status_object:
        for values in i.values():
            if values not in status_lists:
                status_lists.append(values)
    return status_lists

def Level(times=None):
    ###告警等级
    level_lists = list()
    level_object = Alerts.objects.filter(times__contains=times).values('level')
    for i in level_object:
        for values in i.values():
            if values not in level_lists:
                level_lists.append(values)
    return level_lists

####################接受告警短信整理
def Host_send(hostname=None):
    result = ','.join(hostname)
    return  result

def Message_send(message=None):
    result = ','.join(message)
    return  result

def Status_send(status=None):
    result = ','.join(status)
    return  result

def Level_send(level=None):
    result = ','.join(level)
    return  result

