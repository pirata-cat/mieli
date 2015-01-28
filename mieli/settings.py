"""
THIS IS AN AUTO-GENERATED FILE. CHANGES YOU MAKE HERE WILL BE OVERWRITTEN
IF YOU WANT TO INTRODUCE MODIFICATIONS EDIT THE settings.py.j2 FILE
LOCATED IN THE deploy/roles/application/templates/django DIRECTORY.
"""

import os
from datetime import timedelta

# The base dir is the parent of the directory. If we were to change the inner
# dirname to abspath we would have to append "..".
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = "canihazchangeplz?"

DEBUG = True
TEMPLATE_DEBUG = True

# django will recursively search in directories for other template folders
TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)

ALLOWED_HOSTS = []
ROOT_URLCONF = 'mieli.urls'

WSGI_APPLICATION = 'mieli.wsgi.application'

# Installed apps
DEFAULT_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
)

FIRST_PARTY_APPS = (
    'mieli',
    'identity',
)

THIRD_PARTY_APPS = (
    'gunicorn',
)

INSTALLED_APPS = DEFAULT_APPS + FIRST_PARTY_APPS + THIRD_PARTY_APPS


# Middleware classes
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)


#Template context processors
DEFAULT_TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.debug",
)

CUSTOM_TEMPLATE_CONTEXT_PROCESSORS = ()

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_TEMPLATE_CONTEXT_PROCESSORS + CUSTOM_TEMPLATE_CONTEXT_PROCESSORS


# Static file configuration
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'


# Media files configuration
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mieli',
        'USER': 'mieli',
        'PASSWORD': 'mieli',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

#  Optimizes read heavy PG workload, install only if PG
if 'postgresql_psycopg2' == 'postgresql_psycopg2':
    DATABASES['default']['OPTIONS'] = {'autocommit': True}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = False
USE_TZ = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': [],
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}
