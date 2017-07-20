# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from datetime import timedelta

from celery.schedules import crontab

from .base import *

SECRET_KEY = ''


# Security
# ------------------------------------------------------------------------------

SECURE_SSL_HOST = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# Email settings
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = 'Sentinel <noreply@%s>' % WEBSITE_DOMAIN
EMAIL_BACKEND = 'django_mailgun.MailgunBackend'

MAILGUN_ACCESS_KEY = ''
MAILGUN_SERVER_NAME = ''
SERVER_EMAIL = DEFAULT_FROM_EMAIL


# Template settings
# ------------------------------------------------------------------------------
# See:
# https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.cached.Loader
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader', ]),
]


# Caching
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,  # mimics memcache behavior.
                                        # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
        }
    }
}


# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------

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


# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console', 'mail_admins'],
            'propagate': True
        }
    }
}


# DJANGO COMPRESSOR
# ------------------------------------------------------------------------------

COMPRESS_OFFLINE = True


# Opbeat
# ------------------------------------------------------------------------------

INSTALLED_APPS += ('opbeat.contrib.django', )
MIDDLEWARE += ['opbeat.contrib.django.middleware.OpbeatAPMMiddleware', ]

OPBEAT = {}


# Google Tag Manager
# ------------------------------------------------------------------------------

GOOGLE_TAG_MANAGER_KEY = ''


# CELERY
# ------------------------------------------------------------------------------

BROKER_URL = 'redis://localhost:6379/2'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'


# CUSTOM CONFIGURATION
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------

try:
    from .production_local import *
except ImportError:
    pass
