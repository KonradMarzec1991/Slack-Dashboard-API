"""
Django settings for slack_app project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a&u2n^+q!r^-e=m0yta%%av2e33h%2!biwv^di5j*3+++zje_#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '*'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'drf_yasg',
    'celery',
]

MY_APPS = [
    'tickets',
    'status',
]

INSTALLED_APPS += MY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'slack_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'slack_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': os.environ.get('POSTGRES_ENGINE', "django.db.backends.postgresql"),
        'NAME': os.environ.get('POSTGRES_DATABASE', 'tickets_db'),
        'USER': os.environ.get('POSTGRES_USER', 'tickets'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'tickets123'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', 5432),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_files')
]

COMMIT = os.getenv('COMMIT', '2874#952')
VERSION = os.getenv('VERSION', '1.0.0')

URL_PREFIX = 'api/'

CELERY_BROKER_URL = 'redis://rd01:6379/0'
CELERY_RESULT_BACKEND = 'redis://rd01:6379/0'

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

# LOGGING SETTINGS
PROD_LOG_LEVEL = 'INFO'
DEBUG_LOG_LEVEL = 'DEBUG'

_COMMON_LOG_LEVEL = DEBUG_LOG_LEVEL if DEBUG else PROD_LOG_LEVEL

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
LOG_FILE_NAME = 'tickets.log'

LOG_FILE_SIZE = 16  # MB
LOG_FILE_BACKUPS = 1

COMMON_LOG_HANDLERS = ('console', 'file')


def downgrade_info_to_debug(record):
    import logging
    if record.levelno == logging.INFO:
        record.levelno = logging.DEBUG
        record.levelname = 'DEBUG'
    return True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'long': {
            'format': '[%(levelname)s][%(asctime)s][%(name)s]%(message)s'
        },
        'short': {
            'format': '[%(levelno)s][%(asctime)s][%(name)s]%(message)s'
        }
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'downgrade_info_to_debug': {
            '()': lambda: downgrade_info_to_debug,
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler'
        },
        'file': {
            'level': _COMMON_LOG_LEVEL,
            'class': 'slack_app.handlers.MakeFileHandler',
            'formatter': 'long',
            'filename': os.path.join(LOG_DIR, LOG_FILE_NAME),
            'encoding': 'UTF-8',
            'maxBytes': LOG_FILE_SIZE * 1024 * 1024,
            'backupCount': LOG_FILE_BACKUPS,
            'delay': True
        },
        'console': {
            'level': _COMMON_LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'short'
        }
    },
    'loggers': {
        'django': {
            'handlers': COMMON_LOG_HANDLERS,
            'level': 'WARNING',
            'propagate': False
        },
        'django.request': {
            'level': 'WARNING' if DEBUG else 'ERROR',
            'handlers': COMMON_LOG_HANDLERS,
            'propagate': False
        },
        'django.db.backends': {
            'level': 'INFO',
            'handlers': COMMON_LOG_HANDLERS,
            'propagate': False
        },
        'py.warnings': {
            'handlers': COMMON_LOG_HANDLERS if DEBUG else []
        },
        'server': {
            'level': _COMMON_LOG_LEVEL,
            'handlers': COMMON_LOG_HANDLERS,
            'propagate': False
        }
    },
}

# SET LOGGING SETTINGS to each APP
MY_LOGGERS = dict()
for app in MY_APPS:
    MY_LOGGERS[app] = {
        'level': _COMMON_LOG_LEVEL,
        'handlers': COMMON_LOG_HANDLERS
    }
LOGGING['loggers'].update(MY_LOGGERS)