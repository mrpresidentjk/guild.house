# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf import settings


DEBUG = getattr(settings, 'DEBUG', False)
