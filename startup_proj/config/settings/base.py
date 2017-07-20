import environ

ROOT_DIR = environ.Path(__file__) - 3  # (/a/b/myfile.py - 3 = /)
APPS_DIR = ROOT_DIR.path('app')

env = environ.Env()

# WEBSITE
# ------------------------------------------------------------------------------

WEBSITE_NAME = 'Startup'
WEBSITE_DOMAIN = 'example.com'  # Not include subdomain
WEBSITE_URL = 'http://www.' + WEBSITE_DOMAIN


# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'compressor',
    'django_extensions',
    'sass_processor',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'app',
    'app.common',
    'app.pages',

)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {
    'sites': 'app.contrib.sites.migrations'
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
    ("""Administrator""", 'admin@example.com'),
)

MANAGERS = ADMINS


# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------

TIME_ZONE = 'UTC'  # or 'Asia/Bangkok'

LANGUAGE_CODE = 'en-us'  # or 'th'

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

                # Custom context processors
                'app.context_processors.project_settings',
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
    'sass_processor.finders.CssFinder',
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
