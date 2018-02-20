# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import settings


def show_toolbar(request):
    if request.is_ajax():
        return False
    return settings.DEBUG
