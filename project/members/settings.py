# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf import settings


PAYMENT_METHODS = getattr(settings, 'MEMBERS_PAYMENT_METHODS', [
    ('paypal', 'paypal'),
    ('in person', 'in person'),
])


MEMBERS_TYPES = getattr(settings, 'MEMBERS_TYPES', [
    ('standard', 'Guild Member'),
    ('family', 'Guild Member Family'),
    ('student', 'Guild Student Member'),
    ('special', 'other'),
])
