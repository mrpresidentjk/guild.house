# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .base import *  # NOQA


DEBUG = False
THUMBNAIL_DEBUG = DEBUG
ALLOWED_HOSTS = ['guild.house', 'guild.clients.mattaustin.com.au']


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'guild.house',
        'CONN_MAX_AGE': 600,
    }
}


# Email

EMAIL_HOST = 'localhost'

EMAIL_PORT = 25


# Sessions

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True


# Storage

DEFAULT_FILE_STORAGE = 'project.settings.storage.PublicMediaS3BotoStorage'


# Raven

RAVEN_CONFIG = {
    'dsn': 'http://52a09f20f1344361871c44bf82ec4446:a4ef7a7027024fda9d3dd23aca77ec0c@sentry.mattaustin.me.uk/11',  # NOQA
}
