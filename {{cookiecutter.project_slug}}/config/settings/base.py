"""
Settings for {{cookiecutter.project_name}}

Django settings documentation
https://docs.djangoproject.com/en/dev/topics/settings/

Django settings reference
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import environ

ROOT_DIR = environ.Path(__file__) - 3  # (/a/b/myfile.py - 3 = /)
APPS_DIR = ROOT_DIR.path('app')

env = environ.Env()
READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)

if READ_DOT_ENV_FILE:
    # Operating System Environment variables have precedence over variables defined in the .env file,
    # that is to say variables from the .env files will only be used if not defined
    # as environment variables.
    env_file = str(ROOT_DIR.path('.env'))
    print('Loading : {}'.format(env_file))
    env.read_env(env_file)
    print('The .env file has been loaded.')


WEBSITE_NAME = '{{cookiecutter.project_name}}'
WEBSITE_DOMAIN = '{{cookiecutter.domain_name}}'  # Do not include subdomain
WEBSITE_URL = 'http://' + WEBSITE_DOMAIN


# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.facebook',
    #
    # 'bootstrap3',
    # 'compressor',
    # 'crispy_forms',
    # 'easy_thumbnails',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    # '{{cookiecutter.project_slug}}.useraccount',  # custom users app
    'app.pages',

)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', False)


# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
FIXTURE_DIRS = (
    str(APPS_DIR.path('fixtures')),
)


# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')


# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
ADMINS = (
    ("""{{cookiecutter.admin_name}}""", '{{cookiecutter.admin_email}}'),
)

MANAGERS = ADMINS


# DATABASE
# ------------------------------------------------------------------------------
DATABASES = {
    'default': env.db('DATABASE_URL', default='sqlite:///database.db'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True


# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
TIME_ZONE = '{{ cookiecutter.timezone }}'
LANGUAGE_CODE = '{{cookiecutter.language_code}}'

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
)


# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------

MEDIA_ROOT = str(APPS_DIR('media'))
MEDIA_URL = '/media/'


# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

ADMIN_URL = r'^admin/'


# PASSWORD STORAGE SETTINGS
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]


#
#
# # CRISPY FORM
# # ------------------------------------------------------------------------------
#
# CRISPY_TEMPLATE_PACK = 'bootstrap3'
#
#
# # UPLOAD
# # ------------------------------------------------------------------------------
#
# UPLOAD_SETTINGS = {
#     'user_profile': {
#         'max_size_in_mb': 5,
#         'max_size_in_bytes': 1024 * 1024 * 5,
#         'accepted_file': 'image/*'
#     }
# }
#
#
# # EASY THUMBNAILS
# # ------------------------------------------------------------------------------
#
# THUMBNAIL_SAVE_ORIGINAL = {
#     'user_profile': {'size': (1024, 1024)}
# }
#
# THUMBNAIL_ALIASES = {
#     '': {
#         'user_profile_uploader_thumbnail': {'size': (120, 120), 'crop': True},
#
#
#     },
#     'useraccount.User.profile_image': {
#         'square_120': {'size': (120, 120), 'crop': True},
#
#     },
# }
#
# EMPTY_THUMBNAIL_ALIASES = {
#     'useraccount.User.profile_image': {
#         'filepath': 'images/users/user_profile/empty.jpg',
#     },
# }
#
# # DJANGO COMPRESSOR
# # ------------------------------------------------------------------------------
#
# COMPRESS_OFFLINE = True
#
#
# # Your common stuff: Below this line define 3rd party library settings
#
# TEMP_PROFILE_IMAGE_DIR = 'users/temp/avatar'
# TEMP_PROFILE_IMAGE_FILE_TYPE = 'jpg'
