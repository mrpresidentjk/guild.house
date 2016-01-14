# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import settings


def debug(request):
    return {'debug': settings.DEBUG}
