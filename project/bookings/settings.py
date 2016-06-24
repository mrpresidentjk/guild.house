# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf import settings


BOOKINGS_PAGINATE_BY = getattr(settings, 'BOOKINGS_BOOKING_PAGINATE_BY', 100)

BOOKINGS_FEED = getattr(settings, 'BOOKINGS_BOOKING_FEED', 10)

# If a booking is greater or equal to this number it is treated as a larger sized booking.
BIG_BOOKING = getattr(settings, 'BOOKINGS_BIG_BOOKING', 10)

TIME_ZONE = settings.TIME_ZONE

DEFAULT_BOOKING_TIME = getattr(settings, 'BOOKINGS_DEFAULT_BOOKING_TIME', "18:30")

DEFAULT_CALENDAR_LENGTH = getattr(settings, 'BOOKINGS_DEFAULT_CALENDAR_LENGTH', 42)

FROM_EMAIL = getattr(settings, 'DEFAULT_FROM_EMAIL')

TO_EMAILS = getattr(settings, 'BOOKINGS_TO_EMAILS')