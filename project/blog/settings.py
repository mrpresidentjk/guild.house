# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf import settings


ENTRIES_PAGINATE_BY = getattr(settings, 'BLOG_ENTRIES_PAGINATE_BY', 10)

ENTRIES_FEED = getattr(settings, 'BLOG_ENTRIES_FEED', 10)

TIME_ZONE = settings.TIME_ZONE
