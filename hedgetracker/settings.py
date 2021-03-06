"""
Django settings for hedgetracker project.

Generated by 'django-admin startproject' using Django 1.11.29.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

from __future__ import absolute_import
import sys
sys.path.append('/app/main/bchd/protobuf')

import os
import grpc
import redis
from decouple import config
import bchrpc_pb2_grpc as bchrpc
from celery.schedules import crontab


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o1c_@qmnp0^)r5n8m7v3=#l*3x7jioraem+)yx=c=bj2&#*6(f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'channels',
    'main',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hedgetracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'hedgetracker.wsgi.application'
ASGI_APPLICATION = 'hedgetracker.asgi.application'


if DEBUG:
    CORS_ORIGIN_ALLOW_ALL = True
else:
    CORS_ORIGIN_WHITELIST = []


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('POSTGRES_DB', default='hedgetracker'),
        'HOST': config('POSTGRES_HOST', default='localhost'),
        'PORT': config('POSTGRES_PORT', default=5432, cast=int),
        'USER': config('POSTGRES_USER', default='postgres'),
        'PASSWORD': config('POSTGRES_PASSWORD', default='badpassword')
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEPLOYMENT_INSTANCE = config('DEPLOYMENT_INSTANCE', default='dev')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Logging settings

DJANGO_LOG_LEVEL = 'INFO'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '[%(asctime)s %(levelname)s] [%(pathname)s:%(lineno)d] - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
    },
    'loggers': {
        '': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False
        },
        'django': {
            'handlers': ['console'],
            'level': DJANGO_LOG_LEVEL,
            'propagate': False
        },
        'main': {
            'handlers': ['console'],
            'level': DJANGO_LOG_LEVEL,
            'propagate': False
        },
        'django.template': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        }
    },
}

# BCHD settings

BCHD_GRPC_URL = config('BCHD_GRPC_URL', default='bchd.fountainhead.cash')
BCHD_SSL_CERT_PATH = os.path.join(BASE_DIR, 'bchd.crt')

if os.path.exists(BCHD_SSL_CERT_PATH):
    cert = open(BCHD_SSL_CERT_PATH, 'rb').read()
    creds = grpc.ssl_channel_credentials(cert)
else:
    creds = grpc.ssl_channel_credentials()

GRPC_CHANNEL = grpc.secure_channel(BCHD_GRPC_URL, creds)
GRPC_STUB = bchrpc.bchrpcStub(GRPC_CHANNEL)


# REST API and django-filters settings

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication'
    ],
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10,

    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ]
}

# Django-Channels settings

MAIN_ROOM = 'main_room'
MAIN_CHANNEL = 'detoken'


REDIS_HOST = config('REDIS_HOST', default='localhost')
REDIS_PASSWORD = config('REDIS_PASSWORD', default='')
REDIS_PORT = config('REDIS_PORT', default=6379)

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(REDIS_HOST, REDIS_PORT)],
        },
    }
}


OPERATIONS = {
    'SETTLEMENT': 'settlement',
    'METRIC': 'metric'
}

SATOSHI_DECIMAL = 100000000


# Celery settings

CELERY_IMPORTS = ('main.tasks', )

DB_NUM = [0,1,3]

if DEPLOYMENT_INSTANCE == 'dev':
    DB_NUM = [4,5,6]


if REDIS_PASSWORD:
    CELERY_BROKER_URL = 'redis://user:%s@%s:%s/%s' % (REDIS_PASSWORD, REDIS_HOST, REDIS_PORT, DB_NUM[0])
    CELERY_RESULT_BACKEND = 'redis://user:%s@%s:%s/%s' % (REDIS_PASSWORD, REDIS_HOST, REDIS_PORT, DB_NUM[1])

    REDISKV = redis.StrictRedis(
        host=REDIS_HOST,
        password=REDIS_PASSWORD,
        port=6379,
        db=DB_NUM[2]
    )
else:
    CELERY_BROKER_URL = 'redis://%s:%s/%s' % (REDIS_HOST, REDIS_PORT, DB_NUM[0])
    CELERY_RESULT_BACKEND = 'redis://%s:%s/%s' % (REDIS_HOST, REDIS_PORT, DB_NUM[1])

    REDISKV = redis.StrictRedis(
        host=REDIS_HOST,
        port=6379,
        db=DB_NUM[2]
    )

CELERY_TASK_ACKS_LATE = True
CELERYD_PREFETCH_MULTIPLIER = 1
CELERYD_MAX_TASKS_PER_CHILD = 5

CELERY_BEAT_SCHEDULE = {
    'compute-metrics': {
        'task': 'main.tasks.compute_metrics',
        'schedule': crontab(hour=23, minute=50)
    },
}
