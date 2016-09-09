# -*- coding: utf-8 -*-
from datetime import time
from django.conf import settings


BOOKINGS_PAGINATE_BY = getattr(settings, 'BOOKINGS_BOOKING_PAGINATE_BY', 100)

BOOKINGS_FEED = getattr(settings, 'BOOKINGS_BOOKING_FEED', 10)

# If a booking is greater or equal to this number it is treated as a larger sized booking.
BIG_BOOKING = getattr(settings, 'BOOKINGS_BIG_BOOKING', 7)

TIME_ZONE = settings.TIME_ZONE

DEFAULT_BOOKING_TIME = getattr(settings, 'BOOKINGS_DEFAULT_BOOKING_TIME', "18:00")

DEFAULT_BOOKING_DURATION = getattr(settings, 'BOOKINGS_DEFAULT_BOOKING_DURATION',
                                   "00:01:45")

DEFAULT_CALENDAR_LENGTH = getattr(settings, 'BOOKINGS_DEFAULT_CALENDAR_LENGTH', 42)

FROM_EMAIL = getattr(settings, 'DEFAULT_FROM_EMAIL')

TO_EMAILS = getattr(settings, 'BOOKINGS_TO_EMAILS')

STATUS_CHOICES = [
    ('Added', 'Added'),
    ('Confirmed', 'Confirmed'),
    ('Numbers Confirmed', 'Numbers Confirmed'),
    ('Big Booking', 'Big Booking'),
    ('Cancelled', 'Cancelled'),
]

METHOD_CHOICE = [
    ('phone', 'Phone'),
    ('email', 'Email'),
    ('website', 'Online'),
    ('facebook', 'Facebook Messenger'),
    ('person', 'In Person'),
    ('other', 'Other'),
]

SERVICE_CHOICE = [
    ('lunch', 'Lunch'),
    ('afternoon', 'Afternoon'),
    ('main', 'Main'),
]

SERVICE_TIMES = [
    (time(12), 'lunch'),
    (time(15), 'afternoon'),
    (time(17,30), 'main'),
]

DURATION_SELECTION = [
    ('00:00:15', '15 minutes'),
    ('00:00:30', '30 minutes'),
    ('00:00:45', '45 minutes'),
    ('00:01:00', '1 hour'),
    ('00:01:15', '1 hour and 15 minutes'),
    ('00:01:30', '1 and a half hours'),
    ('00:01:45', '1 hour and 45 minutes'),
    ('00:02:00', '2 hour'),
    ('00:02:30', '2 and a half hours'),
    ('00:03:00', '3 hours'),
    ('00:23:59', 'more than 3 hours')
]

HEAR_CHOICE = [
    ("event", "event"),
    ("facebook", "facebook"),
    ("friends", "friends"),
    ("newspaper", "newspaper"),
    ("search", "search"),
    ("other", "other")
]