# -*- coding:utf-8 -*-


from django.utils import timezone
from django.conf  import settings



def date_expired_default():
    # 用户相关的工具
    # try:
    #     years = int(settings.DEFAULT_EXPIRED_YEARS)
    # except TypeError:
    years = 70
    return timezone.now() + timezone.timedelta(days=365*years)
