#-*-coding:utf-8-*-
from __future__ import absolute_import

from celery import shared_task
from Free.celery import app
import requests
from Free.settings import SELF_IP
from comptroller.models import OperationModel
from accounts.models import Profile

def send_request(url):
    try:
        headers = {'content-type': 'application/json'}
        print url
        requests.get(url)
        requests.keep_alive = False
    except Exception, e:
        print traceback.format_exc()
        logger.error('send request error ,the url is : ' + url + traceback.format_exc())

@app.task(bind=True)
def check_date(self):
    url = SELF_IP + '/assets/check_date/'
    send_request(url)


@app.task(bind=True)
def update_data(self):
    url = SELF_IP + "/assets/update_data/"
    profile = Profile.objects.get(pk=1)
    print 3333,url
    OperationModel.objects.create(pro=profile, user_name=profile.name, opt_type='更新记录', opt_content='更新阿里云服务器信息')
    send_request(url)


@app.task(bind=True)
def update_qcloud(self):
    url = SELF_IP + "/assets/update_qcloud/"
    send_request(url)


@app.task(bind=True)
def update_rds(self):
    url = SELF_IP + "/assets/update_rds/"
    send_request(url)


@app.task(bind=True)
def update_select(self):
    url = SELF_IP + "/assets/update_select/"
    send_request(url)


# 为了省事,把openstack的云服务器信息轮询放到这里了
@app.task(bind=True)
def update_openstack(self):
    url =  SELF_IP + '/nova/update_server'
    send_request(url)

