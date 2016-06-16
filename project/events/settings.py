# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf import settings


EVENTS_PAGINATE_BY = getattr(settings, 'EVENTS_PAGINATE_BY', 10)

EVENTS_FEED = getattr(settings, 'EVENTS_FEED', 10)

TIME_ZONE = settings.TIME_ZONE
