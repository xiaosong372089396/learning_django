#-*-coding:utf-8-*-
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.utils import six
from django.utils.encoding import force_text
from models import ServersModel, ItemList, AliyunTemplate
from models import ServerConf, QcloudTemplate
from accounts.models import Profile

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import hashlib,requests,sys
from info import *
import datetime
import time
import re
import logging
import traceback

logger = logging.getLogger("free")

def Message(mobile,content):
    url = 'http://msgapi.ixianlai.com/smsgateway/msg/serverSendMsg'
    key = '3529632d9f0cb3c87951baf93b94bf0c'
    tel = mobile
    cst_id = '55555'
    md5 = tel + cst_id + key
    hash = hashlib.md5()
    hash.update(md5.encode('utf-8'))
    sign = hash.hexdigest()
    payload = {'cst_id': cst_id, 'sign': sign, 'tel': tel, 'content': content}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
    ret = requests.post(url, data=payload,headers=headers)
    return (ret.text)


def send_alarm(content, phone=''):
    try:
        if phone:
            Message(phone, content)
        else:
            peoples = Profile.objects.filter(send_alarm=True)
            for one in peoples:
                if one.send_alarm:
                    Message(one.cell, content)
    except Exception, e:
        logger.error('发送警报出错了, 内容是:' + content + '错误是:' + traceback.format_exc())


class AccessMixin(object):
    """
    Abstract CBV mixin that gives access mixins the same customizable
    functionality.
    """
    login_url = None
    permission_denied_message = ''
    raise_exception = False
    redirect_field_name = REDIRECT_FIELD_NAME

    def get_login_url(self):
        """
        Override this method to override the login_url attribute.
        """
        login_url = self.login_url or settings.LOGIN_URL
        if not login_url:
            raise ImproperlyConfigured(
                '{0} is missing the login_url attribute. Define {0}.login_url, settings.LOGIN_URL, or override '
                '{0}.get_login_url().'.format(self.__class__.__name__)
            )
        return force_text(login_url)

    def get_permission_denied_message(self):
        """
        Override this method to override the permission_denied_message attribute.
        """
        return self.permission_denied_message

    def get_redirect_field_name(self):
        """
        Override this method to override the redirect_field_name attribute.
        """
        return self.redirect_field_name

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())



class LoginRequiredMixin(AccessMixin):
    """
    CBV mixin which verifies that the current user is authenticated.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return self.handle_no_permission()
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


def send_mail(receiver, title, content):
    mail_host="smtp.exmail.qq.com"  #设置服务器
    mail_user="free@ixianlai.com"    #用户名
    mail_pass="Free123456"   #口令 


    sender = 'free@ixianlai.com'
    receivers = [receiver,]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header(title, 'utf-8')
    message['To'] =  Header(receiver, 'utf-8')

    subject = title
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        return "邮件发送成功"
    except smtplib.SMTPException:
        print  traceback.format_exc()
        send_alarm('发送邮件失败', '18513950766')


#查询数据库，获取不同查询条件查询得数据
def get_servers(query_key, query_value, server_type):
    query_item = ['实例名称', '实例ID', '私有IP', '内网IP', '外网IP', '即将到期', '分组', '未初始化']
    if not query_key and not query_value:
        results = ServersModel.objects.all()
    elif query_key != u'即将到期' and not query_key:
        results = ServersModel.objects.all()
    elif query_key == u'实例名称':
        results = ServersModel.objects.filter(instance_name__contains=query_value)
    elif query_key == u'实例ID':
        query_item[0], query_item[1] = query_item[1], query_item[0]
        results = ServersModel.objects.filter(instanceid__contains=query_value)
    elif query_key == u'未初始化':
        query_item[0], query_item[7] = query_item[7], query_item[0]
        results = ServersModel.objects.filter(mem="未初始化")
        query_value= ""
    elif query_key == u'私有IP':
        query_item[0], query_item[2] = query_item[2], query_item[0]
        results = ServersModel.objects.filter(vpc_private_ip__contains=query_value)
    elif query_key == u'内网IP':
        query_item[0], query_item[3] = query_item[3], query_item[0]
        results = ServersModel.objects.filter(inner_ip__contains=query_value)
    elif query_key == u'外网IP':
        query_item[0], query_item[4] = query_item[4], query_item[0]
        results = ServersModel.objects.filter(public_ip__contains=query_value)
    elif query_key == u"分组":
        query_item[0], query_item[6] = query_item[6], query_item[0]
        results = ServersModel.objects.filter(server_group__name__contains=query_value)
    elif query_key == u'即将到期':
        query_item[0], query_item[5] = query_item[5], query_item[0]
        results = ServersModel.objects.filter(status_color="red")
        query_value = ""
    results = results.filter(server_from=server_type)
    return results, query_item, query_value

#验证阿里云服务器名称的正则
def check_name(name):
    if name.startswith("http://") or name.startswith("https://"):
        return True
    name = name.decode("utf8")
    pat = re.match(ur'^[a-zA-Z\u4e00-\u9FFF][\u3400-\u9FFFA-Za-z0-9_.-]{1,200}$', name)
    if not pat:
        return True
    else:
        return False

#拼接错误信息
def serialize_form_errors(form):
    errors = []
    for field in form:
        if field.errors:
            errors.append(field.label + ':' + ','.join([err for err in field.errors]))
    return '\n'.join(errors)


#查询员工物品单
def get_item(query_value, query_type):
    if query_value in ('', '全部'):
        item_list = ItemList.objects.filter().order_by("is_return")
    else:
        item_list = ItemList.objects.filter(item_type=query_value).order_by('is_return')
        query_index = query_type.pop(query_type.index(query_value))
        query_type = [query_index, ] + query_type
    return item_list, query_type


#初始化sql，主要是server_template
def init_sql():
    confs = ServerConf.objects.all().count()
    aliyun_infos = {'image': IMAGE_INFO, 'server_type': INSTANCETYPE,'io_server_type': IO_INSTANCETYPE, 'rds_class': RDS_CLASS, 'zone': ALIYUN_ZONE}
    qcloud_infos = {'image': QCLOUD_IMAGES,'zone': QCLOUD_ZONE, 'zone_g2': G2, 'zone_g3': G3, 'zone_s1': S1, 'zone_b1': B1, 'zone_x1': X1}
    if int(confs) < 10:
        for one_key, one in aliyun_infos.items():
            for items in one:
                for key, value in items.items():
                    item = ServerConf.objects.create(server_type='aliyun', info_type = one_key, key= key, value= value)
                    item.save()
        for one_key, one in qcloud_infos.items():
            for items in one:
                for key, value in items.items():
                    item = ServerConf.objects.create(server_type='qcloud', info_type = one_key, key= key, value= value)
                    item.save()

    else:
        aliyun_templates = AliyunTemplate.objects.filter(tem_type="aliyun").count()
        if int(aliyun_templates) < 3:
            for one in ALIYUBTEM:
                item = AliyunTemplate.objects.create(zone_id=one[0], cpu=one[1], mem=one[2], image=one[3], bandwidth_paytype=one[4], bandwidth=one[5], root_disk=one[6], data_disk=one[7],
                                                    name=one[8], tem_type="aliyun")
                item.save()
        qcloud_templates = AliyunTemplate.objects.filter(tem_type='qcloud').count()
        if int(qcloud_templates) < 3:
            for one in QCLOUDTEM:
                item = item = AliyunTemplate.objects.create(zone_id=one[0], cpu=one[1], mem=one[2], image=one[3], bandwidth_paytype=one[4], bandwidth=one[5], root_disk=one[6], data_disk=one[7],
                                                    name=one[8], tem_type='qcloud')
                item.save()


#判断是否有访问的权限
def control_permission(level):
    def _control(func):
        def __control(self, request):
            if self.request.user.profile.privilege < int(level):
                raise PermissionDenied('不许偷食禁果')
            else:
                return func(self, request)
        return __control
    return _control


#for get_context_data
def control_permission_context(level):

    def _control(func):
        def __control(self, **kwarg):
            if self.request.user.profile.privilege < int(level):
                raise PermissionDenied('不许偷食禁果')
            else:
                return func(self, **kwarg)
        return __control
    return _control


ALIYUBTEM = [('cn-hangzhou-c', '16', '16', '游戏项目自定义镜像', 'PayByTraffic', '100', '100', '0','_Center_1'),
( 'cn-hangzhou-c', '16', '16', '游戏项目自定义镜像', 'PayByTraffic', '100', '100', '0', '_LD_LM_1'),
('cn-hangzhou-c', '4', '4', '游戏项目自定义镜像', 'PayByTraffic', '100', '100', '0', '_Logic_1'),
('cn-hangzhou-c', '4', '4', '游戏项目自定义镜像', 'PayByTraffic', '100', '100', '0', '_Gate_1'),
('cn-hangzhou-c', '4', '4', '游戏项目自定义镜像', 'PayByTraffic', '100', '100', '0', '_Login_1')]


QCLOUDTEM = [('上海一区', '16', '16', 'Centos6.5', '按流量付费', '100', '20', '100','_Center_1'),
( '上海一区', '16', '16', 'Centos6.5', '按流量付费', '100', '20', '100', '_LD_LM_1'),
('上海一区', '4', '4', 'Centos6.5', '按流量付费', '100', '20', '100', '_Logic_1'),
('上海一区', '4', '4', 'Centos6.5', '按流量付费', '100', '20', '100', '_Gate_1'),
('上海一区', '4', '4', 'Centos6.5', '按流量付费', '100', '20', '100', '_Login_1')]
