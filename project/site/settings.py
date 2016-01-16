# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf import settings


HOMEPAGE_CATEGORIES = getattr(settings, 'SITE_HOMEPAGE_CATEGORIES', 10)

HOMEPAGE_GAMES = getattr(settings, 'SITE_HOMEPAGE_GAMES', 10)
