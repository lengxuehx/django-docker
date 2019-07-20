# -*- coding: utf-8 -*-
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = False

DJANGO_REQ_ERROR_LOG = os.path.join(BASE_DIR, "req_error.log")
DEBUG_LOG = os.path.join(BASE_DIR, "debug.log")
COMMON_REST_LOG = os.path.join(BASE_DIR, "common_rest.log")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'raven.contrib.django.raven_compat',
    'corsheaders',
    'watchman',

    'myapp'
]

MIGRATION_MODULES = {
    'animation_pipeline': 'migrations.animation_pipeline',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.QueryParameterVersioning',
    'DEFAULT_THROTTLE_RATES': {
        'phone_throttle': {"second": 1, "minute": 7, "day": 50},
        'ip_throttle': {"second": 100},
    }
}

DATA_UPLOAD_MAX_MEMORY_SIZE = None

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = False

USE_TZ = False

DATETIME_INPUT_FORMATS = [
    '%Y-%m-%dT%H:%M:%S',
    '%Y-%m-%dT%H:%M:%S.%f',
    '%Y-%m-%d %H:%M:%S',
    '%Y-%m-%d %H:%M:%S.%f',
    '%Y-%m-%d %H:%M',
    '%Y-%m-%d'
]

import socket
import os
import sys

socket.setdefaulttimeout(30)

_curdir = os.path.dirname(os.path.dirname(__file__))
_libs_dir = os.path.join(_curdir, 'libs')
if os.path.isdir(_libs_dir):
    sys.path.append(_libs_dir)
    for _file in os.listdir(_libs_dir):
        if _file.endswith('.zip'):
            sys.path.append(os.path.join(_libs_dir, _file))

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_CACHE_ALIAS = 'default'
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'


STATIC_URL = '/static/'
STATIC_ROOT = './staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/opt/media/virtualx_server'

CORS_ORIGIN_ALLOW_ALL = DEBUG

CORS_ALLOW_HEADERS = (
    'content-disposition', 'accept-encoding',
    'content-type', 'accept', 'origin', 'authorization',
    'Platform-AUTHORIZATION', 'APP', 'APPID', 'customer-authorization'
)


def update_configuration():
    try:
        from . import CONFIGS as _configs
    except ImportError:
        _configs = None
    if _configs is None:
        return
    global_variables = globals()
    for setting in dir(_configs):
        if setting == setting.upper():
            setting_value = getattr(_configs, setting)
            global_variables[setting] = setting_value
    global_variables["SERVER_EMAIL"] = global_variables.get("EMAIL_HOST_USER", "notification@xxx.com")
    global_variables["TEMPLATE_DEBUG"] = global_variables.get("DEBUG", False)
    global_variables["MANAGERS"] = global_variables.get("ADMINS", ())

    if os.environ.get('RUN_ENV') == 'DOCKER':
        global_variables['DATABASES'] = global_variables['DOCKER_DATABASES']
    else:
        global_variables['DATABASES'] = global_variables['HOST_DATABASES']


update_configuration()


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)-8s[%(filename)s:%(lineno)d(%(funcName)s)] %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'django_req_error_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': DJANGO_REQ_ERROR_LOG,
            'mode': 'a',
            'maxBytes': 100 * 1024 * 1024,
            'backupCount': 5,
            'encoding': 'utf-8',
            'formatter': 'verbose',
        },
        'common_rest_log_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': COMMON_REST_LOG,
            'mode': 'a',
            'maxBytes': 100 * 1024 * 1024,
            'backupCount': 5,
            'encoding': 'utf-8',
            'formatter': 'verbose',
        },
        'debug_log_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': DEBUG_LOG,
            'mode': 'a',
            'maxBytes': 100 * 1024 * 1024,
            'backupCount': 5,
            'encoding': 'utf-8',
            'formatter': 'verbose',
        },
        'sentry': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'django_req_error_handler'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console', 'sentry'],
            'level': 'WARNING',
            'propagate': False,
        },
        'rest.logger': {
            'handlers': ['common_rest_log_handler', 'sentry', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'common.logger': {
            'handlers': ['debug_log_handler', 'sentry', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django_auth_ldap': {
            'handlers': ['debug_log_handler', 'sentry', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}
