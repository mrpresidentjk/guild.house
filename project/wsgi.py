# -*- coding: utf-8 -*-
"""WSGI config for project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/

"""

from django.core.wsgi import get_wsgi_application
from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
application = Sentry(get_wsgi_application())
