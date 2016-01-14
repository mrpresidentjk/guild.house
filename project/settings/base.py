# -*- coding: utf-8 -*-
"""Django settings for Guild project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/

"""

from __future__ import absolute_import, unicode_literals
import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..')


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd16bx=+!594*6x(v^ba=qj#8u)=zr19c202(6(mu26!rk)vfr3'

ADMINS = (
    ('Matt Austin', 'devops@mattaustin.com.au'),
)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    'debug_toolbar',
    'raven.contrib.django.raven_compat',
    'robots',
    # 'sorl.thumbnail',
    'storages',
    'tinymce',

    'project.admin',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.tz',
                'project.debug_toolbar.context_processors.debug',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-au'

TIME_ZONE = 'Australia/Canberra'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Media files

MEDIA_ROOT = os.path.join(BASE_DIR, 'public/media')

MEDIA_URL = '/media/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'public/static')

STATIC_URL = '/static/'


# Sites framework

SITE_ID = 1


# Email

DEFAULT_FROM_EMAIL = 'devops@mattaustin.com.au'

EMAIL_SUBJECT_PREFIX = '[Guild] '

SERVER_EMAIL = 'devops@mattaustin.com.au'


# Logging
# https://docs.getsentry.com/hosted/clients/python/integrations/django/#integration-with-logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d '
                      '%(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class':
                'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}


# TinyMCE

TINYMCE_DEFAULT_CONFIG = {
    'body_class': 'content',
    # 'content_css': STATIC_URL + 'stylesheets/tinymce.css',
    'plugins': 'charmap code contextmenu fullscreen link paste wordcount',
    'relative_urls': False,
    'statusbar': False,
    'toolbar': 'undo redo | styleselect | bold italic | bullist numlist',
}


# AWS

AWS_ACCESS_KEY_ID = ''  # TODO

AWS_SECRET_ACCESS_KEY = ''  # TODO
