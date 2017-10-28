from __future__ import absolute_import

from celery import shared_task
from Free.celery import app


from zabbix.core import Zabbix


zabbix_celery = Zabbix()


@app.task(bind=True)
def update_host(self):
    zabbix_celery.updatehost()


@app.task(bind=True)
def update_template(self):
    zabbix_celery.update_template()


@app.task(bind=True)
def update_group(self):
    zabbix_celery.update_group()


@app.task(bind=True)
def update_proxy(self):
    zabbix_celery.update_proxy()