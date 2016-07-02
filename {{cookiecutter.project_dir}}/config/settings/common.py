# -*- coding: utf-8 -*-
"""
Django settings for {{cookiecutter.project_slug}} project.

Django settings documentation
https://docs.djangoproject.com/en/dev/topics/settings/

Django settings reference
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from __future__ import absolute_import, unicode_literals

import environ

ROOT_DIR = environ.Path(__file__) - 3  # (/a/b/myfile.py - 3 = /)
APPS_DIR = ROOT_DIR.path('{{cookiecutter.project_slug}}')

env = environ.Env()

WEBSITE_NAME = '{{cookiecutter.project_name}}'
WEBSITE_DOMAIN = '{{cookiecutter.domain_name}}'  # Do not include subdomain
WEBSITE_URL = 'www.' + WEBSITE_DOMAIN


# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Admin
    'django.contrib.admin',
)

THIRD_PARTY_APPS = (
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',

    'bootstrap3',
    'compressor',
    'crispy_forms',
    'easy_thumbnails',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    '{{cookiecutter.project_slug}}.common',
    '{{cookiecutter.project_slug}}.users',  # custom users app

    # Your stuff: custom apps go here


)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES = (
    # Make sure djangosecure.middleware.SecurityMiddleware is listed first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {
    'sites': '{{cookiecutter.project_slug}}.contrib.sites.migrations'
}


# DEBUG
# ------------------------------------------------------------------------------
DEBUG = False


# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
FIXTURE_DIRS = (
    str(APPS_DIR.path('fixtures')),
)


# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''
EMAIL_SUBJECT_PREFIX = ''


# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
ADMINS = (
    ("""{{cookiecutter.admin_name}}""", '{{cookiecutter.admin_email}}'),
)

MANAGERS = ADMINS


# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
TIME_ZONE = 'UTC'

LANGUAGE_CODE = '{{cookiecutter.language_code}}'

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True


# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',

                # Your stuff: custom template context processors go here
                '{{cookiecutter.project_slug}}.context_processors.project_settings',
            ],
        },
    },
]


# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------

STATIC_ROOT = str(ROOT_DIR('staticfiles'))
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    str(APPS_DIR.path('static')),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

    'compressor.finders.CompressorFinder',
)


# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------

MEDIA_ROOT = str(APPS_DIR('media'))
MEDIA_URL = '/media/'


# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = r'^admin/'


# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = 'pages:homepage'
LOGIN_URL = 'account_login'

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False

ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_USER_DISPLAY = '{{cookiecutter.project_slug}}.users.models.user_display_name'

ACCOUNT_FORMS = {
    'signup': '{{cookiecutter.project_slug}}.users.forms.EmailUserSignupForm',
    'reset_password': '{{cookiecutter.project_slug}}.users.forms.ResetPasswordForm',
}

# Email verification
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7

ACCOUNT_LOGIN_ON_PASSWORD_RESET = True

ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = False

# Social account
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_ADAPTER = '{{cookiecutter.project_slug}}.users.adapter.SocialAccountAdapter'

SOCIALACCOUNT_FORMS = {
    'signup': '{{cookiecutter.project_slug}}.users.forms.SocialUserSignupForm',
}

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', 'public_profile'],
        'METHOD': 'oauth2',
        'VERIFIED_EMAIL': True,
    },
}


# CRISPY FORM
# ------------------------------------------------------------------------------

CRISPY_TEMPLATE_PACK = 'bootstrap3'


# UPLOAD
# ------------------------------------------------------------------------------

UPLOAD_SETTINGS = {
    'user_profile': {
        'max_size_in_mb': 5,
        'max_size_in_bytes': 1024 * 1024 * 5,
        'accepted_file': 'image/*'
    }
}


# EASY THUMBNAILS
# ------------------------------------------------------------------------------

THUMBNAIL_SAVE_ORIGINAL = {
    'user_profile': {'size': (1024, 1024)}
}

THUMBNAIL_ALIASES = {
    '': {
        'user_profile_uploader_thumbnail': {'size': (120, 120), 'crop': True},


    },
    'users.User.profile_image': {
        'square_120': {'size': (120, 120), 'crop': True},

    },
}

EMPTY_THUMBNAIL_ALIASES = {
    'users.User.profile_image': {
        'filepath': 'images/users/user_profile/empty.jpg',
    },
}

# DJANGO COMPRESSOR
# ------------------------------------------------------------------------------

COMPRESS_OFFLINE = True


# Your common stuff: Below this line define 3rd party library settings

TEMP_PROFILE_IMAGE_DIR = 'users/temp/avatar'
TEMP_PROFILE_IMAGE_FILE_TYPE = 'jpg'
