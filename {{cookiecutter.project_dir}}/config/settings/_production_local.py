
ALLOWED_HOSTS = ['', ]


# Database settings
# ------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}


# Mailgun
# ------------------------------------------------------------------------------
MAILGUN_ACCESS_KEY = ''
MAILGUN_SERVER_NAME = ''


# Secret key
# ------------------------------------------------------------------------------
# Use http://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = ''
