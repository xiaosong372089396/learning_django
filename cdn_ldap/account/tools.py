# -*- coding:utf-8 -*-

from django.utils import timezone

def date_expired_default():
    # 用户相关工具类
    # try:
    #       years = int(settings.DEFAULT_EXPIRED_YEARS)
    # except TypeError:
    years = 70
    return timezone.now() + timezone.timedelta(days=365 * years)
