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
    ('special', 'other (please add reason at end)'),
])

TEMPORARYMEMBER_FIELDS = [
    'sort_name',
    'ref_name',
    'email',
    'phone',
    'address',
    'postcode',
    'suburb',
    'state',
    'country',
    'dob',
    'year',
    'member_type',
    'payment_method',
    'survey_food',
    'survey_games',
    'survey_hear',
    'survey_suggestions',
]


MEMBER_FIELDS = [
    'sort_name',
    'ref_name',
    'email',
    'phone',
    'address',
    'postcode',
    'suburb',
    'state',
    'country',
    'dob',
    'year',
]


YEAR_CHOICES = [
    (0, "---"),
    (1945, "'Silent' (~ pre-1946)"),
    (1960, "'Boomer' (to ~ early '60s)"),
    (1980, "'Gen X' (to ~ early 80s)"),
    (2000, "'Gen Y' (to ~ early '00s)"),
    (2010, "'Alpha' (from ~ early '00s)"),
]
