from .base import *

DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

ALLOWED_HOSTS = ['*']


# WEBSITE
# ------------------------------------------------------------------------------
WEBSITE_DOMAIN = 'localhost:8000'
WEBSITE_URL = 'http://' + WEBSITE_DOMAIN


# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
SECRET_KEY = env('DJANGO_SECRET_KEY', default='THIS_IS_DUMMY_SECRET_KEY')


# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_HOST = 'localhost'
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
                    default='django.core.mail.backends.console.EmailBackend')


# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}


# django-debug-toolbar
# ------------------------------------------------------------------------------

MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware', )
INSTALLED_APPS += ('debug_toolbar', )

INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]

import socket
import os
# tricks to have debug toolbar when developing with docker
if os.environ.get('USE_DOCKER') == 'yes':
    ip = socket.gethostbyname(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + '1']

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
    # 'SHOW_TOOLBAR_CALLBACK': lambda r: False,
}


# Testing
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

#
# # Facebook App
# # ------------------------------------------------------------------------------
# FACEBOOK_APP_ID = '225585191119533'
# FACEBOOK_SECRET_KEY = '0be20b2acb2df9dd3d869834a429821b'


# CUSTOM CONFIGURATION
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------

try:
    from .develop_local import *
except ImportError:
    pass
