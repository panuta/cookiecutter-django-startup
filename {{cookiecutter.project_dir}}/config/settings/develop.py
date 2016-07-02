# -*- coding: utf-8 -*-
from .common import *

DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

WEBSITE_DOMAIN = 'localhost:8000'

ALLOWED_HOSTS = ['localhost', ]

SECRET_KEY = 'THIS_IS_DUMMY_SECRET_KEY_FOR_DEVELOPMENT_ONLY'


# Database settings
# ------------------------------------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '{{cookiecutter.project_slug}}',
        'USER': '{{cookiecutter.project_slug}}',
        'PASSWORD': '{{cookiecutter.project_slug}}',
        'HOST': '',
        'PORT': '',
    },
}


# Mail settings
# ------------------------------------------------------------------------------
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Caching
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}


# Django Debug Toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INSTALLED_APPS += ('debug_toolbar', )

INTERNAL_IPS = ('127.0.0.1', )

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}


# Testing
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'


# Facebook App
# ------------------------------------------------------------------------------
FACEBOOK_APP_ID = '225585191119533'
FACEBOOK_SECRET_KEY = '0be20b2acb2df9dd3d869834a429821b'


# CUSTOM CONFIGURATION
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------

try:
    from .develop_local import *
except ImportError:
    pass
