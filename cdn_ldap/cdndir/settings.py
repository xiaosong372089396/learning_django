# -*- coding:utf-8 -*-

"""
Django settings for cdndir project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# 用于从LDAP同步账户,登陆验证设置
import ldap
from django_auth_ldap.config import LDAPSearch, PosixGroupType, LDAPSearchUnion, LDAPGroupType,GroupOfNamesType
from django.urls import reverse_lazy  # 逆向解析模块
#

import djcelery
from datetime import timedelta
import logging
djcelery.setup_loader()
BROKER_URL = 'redis://192.168.10.73:6379/0'   # 127.0.0.1:6379/2
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'afmt$&^#d!_fx9pn0ab(89cd3b&d(i^#ie=f(1+x!1ejip1y-9'

SESSION_COOKIE_AGE = 60 * 30
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440 * 2
FILE_UPLOAD_TEMP_DIR = '/tmp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# 用户自定义认证
AUTH_USER_MODEL = 'account.User'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'login',
    'submits',
    'aliapp',
    'ccmapp',
    'white',
    'txnetworks',
    'overseas',
    'djcelery',
    'kombu.transport.redis',
    # 自定义认证引用
    'account.apps.AccountConfig'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cdndir.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cdndir.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cdndir',    # ldapcdn
        'USER': 'cdndir',    # ldapcdn
        'PASSWORD': '123.com',  # 123.com
        'HOST': '192.168.10.138',  # 127.0.0.1
        'POST': '3306'
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s: %(message)s'
        }
    },
    'filters': {
    },
    'handlers': {
        'cdndir': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'error.log'),
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'cdndir': {
            'handlers': ['cdndir'],
            'level': 'DEBUG',
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

# LOGIN_URL = '/login/'
STATIC_URL = '/static/'
STATIC_ROOT = '/static'
STATICFILES_DIRS = (
    "%s/%s" %(BASE_DIR, "static"),
    "%s/%s" %(BASE_DIR, 'uploads'),
)




# 配置session共享
# 另外一个cached_db,这两个的区别是,cache只写缓存,cached_db除了写缓存还同时写数据库,如果对session的安全性要求高可以选择cached_db
# SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# SESSION_COOKIE_NAME = "cdndir"

# 设置session有效期为一天,默认两周
# SESSION_COOKIE_AGE = 86400
# 此配置不能解决跨域问题,但是能解决a.ssotest.net与b.ssotest.net的session共享问题,不加此属性,跨站(非跨域)时,无法传递session
# SESSION_COOKIE_DOMAIN = "192.168.10.138"

CACHES = {
    'default':{
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': [   # 连接1个MC, python-memcached本身又监控,如果连接多个,挂一个MC后,MC会自动请求分配到好的MC上
            '192.168.10.138:11211',    # 127.0.0.1:11211
        ],
        'TIMEOUT': 30,
        'options': {
            'MAX_ENTRIES': 3000
        }
    }
}
# LOGIN_REDIRECT_URL = reverse_lazy('index')
LOGIN_URL = "/account/login/"  # /account/login
# ####  ldap 配置部分BEGIN #####


# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.
AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',  # 配置为先使用LDAP认证,如果通过认证则不在使用后面的认证方式
    'django.contrib.auth.backends.ModelBackend',  # SSO系统中手动创建用户也可以使用,优先级靠后,注意这两行的顺序
)



# LDAP 服务URL
# 公网 120.55.29.254
AUTH_LDAP_SERVER_URI = "ldap://120.55.29.254"   # 192.168.10.8

# DN
# "cn=xiaosong, ou=devops,dc=ixianlai,dc=com"  测试
# "cn=manager,dc=ixianlai,dc=com"
AUTH_LDAP_BIND_DN = "cn=xiaosong,ou=devops,dc=ixianlai,dc=com"


# 密码
# xiaosong cn=密码
# "dc@123456"   manager密码
AUTH_LDAP_BIND_PASSWORD = "xiaosong"


# 搜索条件
# ou=client,dc=ixianlai,dc=com
AUTH_LDAP_USER_SEARCH = LDAPSearchUnion(
    LDAPSearch("ou=devops,dc=ixianlai,dc=com", ldap.SCOPE_SUBTREE, "(uid=%(user)s)"),  # 用户的DN
)
# uid=xiaosong,ou=People,dc=ixianlai,dc=com

# Key为数据库字段名,Value为ldap中字段名,此字典解决django model与ldap字段名可能出现的不一致问题
AUTH_LDAP_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
    "password": "userPassword"
}


# 组权限管理 #
# ou=Group,dc=ixianlai,dc=com   注意Group   G这里大写
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=devops,dc=ixianlai,dc=com", ldap.SCOPE_SUBTREE,"(objectClass=posixGroup)")

# 组的DN是cn=员工,ou=Peopel,dc=ixianlai,dc=com,所以type是cn
AUTH_LDAP_GROUP_TYPE = PosixGroupType(name_attr="cn")

# 直接把ldap的组复制到django一份,和AUTH_LDAP_FIND_GROUP_PERMS互斥,用户每次登陆会根据LDAP来更新数据库的组关系
AUTH_LDAP_MIRROR_GROUPS = True

# 默认从LDAP同步用户
AUTH_LDAP_ALWAYS_UPDATE_USER = True

# AUTH_LDAP_USER_FLAGS_BY_GROUP = { # django admin的is_staff|superuser属性映射为ldap的管理员
#     "is_staff": "cn=liuyao,ou=devops,dc=ixianlai,dc=com",
#     "is_superuser": "cn=liuyao,ou=devops,dc=ixianlai,dc=com"
# }

LOG_LEVEL = 'DEBUG'
LDAP_LOGS = os.path.join(BASE_DIR, 'logs/ldap.log')
stamdard_format = '[%(asctime)s][%(threadName)s:%(thread)d]' + \
                  '[task_id:%(name)s][%(filename)s:%(lineno)d] ' + \
                  '[%(levelname)s]- %(message)s'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {    # 详细
        'format': stamdard_format
        },
    },
    'handlers': {
        'default':{
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LDAP_LOGS,
            'maxBytes': 1024 * 1024 * 100,  # 5MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        '': {    # default 日志,存放于log中
            'handlers': ['default'],
            'level': 'DEBUG',
        },
        'django_auth_ldap': {   # django_auth_ldap模块相关日志打印到console
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,   # 选择关闭继承,不然这个logger继承自默认,日志就会被记录2次了(''一次, 自己一次)
        },
        'django.db.backends': {    # 数据库相关执行过程log打印到console
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}

# ## log 配置部分END ### #