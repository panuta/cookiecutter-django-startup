
ALLOWED_HOSTS = ['', ]


# Database settings
# ------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}


# Secret key
# ------------------------------------------------------------------------------
# Use http://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = ''


# Omise
# ------------------------------------------------------------------------------

OMISE_SECRET_KEY = ''
OMISE_PUBLIC_KEY = ''


# Facebook
# ------------------------------------------------------------------------------

FACEBOOK_APP_ID = ''
FACEBOOK_SECRET_KEY = ''


# LinePay
# ------------------------------------------------------------------------------

LINEPAY_CHANNEL_ID = ''
LINEPAY_CHANNEL_SECRET_KEY = ''


# Mailgun
# ------------------------------------------------------------------------------
MAILGUN_ACCESS_KEY = ''
MAILGUN_SERVER_NAME = ''


# Google Tag Manager
# ------------------------------------------------------------------------------

GOOGLE_TAG_MANAGER_KEY = ''


# Celery
# ------------------------------------------------------------------------------

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


# django-compressor
# ------------------------------------------------------------------------------

from config.settings.base import COMPRESS_OFFLINE_CONTEXT
COMPRESS_OFFLINE_CONTEXT['OMISE_PUBLIC_KEY'] = OMISE_PUBLIC_KEY
