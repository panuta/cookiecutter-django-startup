# from celery.schedules import crontab

from .base import *


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
        'NAME': 'startup',
        'USER': 'startup',
        'PASSWORD': 'startup',
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

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
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


# CELERY
# ------------------------------------------------------------------------------
# BROKER_URL = 'redis://localhost:6379/2'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
#
# CELERYBEAT_SCHEDULE = {
#     'crawl-facebook': {
#         'task': 'app.collector.tasks.crawl_facebook_page_feeds',
#         'schedule': crontab(minute='*/15')  # Every 15 minutes
#     },
# }


# django-sass-processor
# ------------------------------------------------------------------------------

SASS_PROCESSOR_ENABLED = True


# CUSTOM CONFIGURATION
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------

try:
    from .develop_local import *
except ImportError:
    pass
