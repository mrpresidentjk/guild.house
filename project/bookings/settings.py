# -*- coding: utf-8 -*-
from datetime import time, timedelta
from django.conf import settings


BOOKINGS_PAGINATE_BY = getattr(settings, 'BOOKINGS_BOOKING_PAGINATE_BY', 100)

BOOKINGS_FEED = getattr(settings, 'BOOKINGS_BOOKING_FEED', 10)

# If a booking is greater or equal to this number it is treated as a larger sized booking.
BIG_BOOKING = getattr(settings, 'BOOKINGS_BIG_BOOKING', 7)

TIME_ZONE = settings.TIME_ZONE

DEFAULT_BOOKING_TIME = getattr(settings, 'BOOKINGS_DEFAULT_BOOKING_TIME', "18:00")

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

SERVICE_TIMES = {
    time(12,0): SERVICE_CHOICE[0][0],
    time(14,0): SERVICE_CHOICE[1][0],
    time(17,0): SERVICE_CHOICE[2][0],
}

BOOKING_TIMES = (time(12), time(22))
BOOKING_INTERVAL = timedelta(minutes=15)

DEFAULT_BOOKING_DURATION = getattr(settings, 'BOOKINGS_DEFAULT_BOOKING_DURATION',
                                   "01:45:00")

DURATION_SELECTION = [
    ('00:15:00', '15 minutes'),
    ('00:30:00', '30 minutes'),
    ('00:45:00', '45 minutes'),
    ('01:00:00', '1 hour'),
    ('01:15:00', '1 hour and 15 minutes'),
    ('01:30:00', '1 and a half hours'),
    ('01:45:00', '1 hour and 45 minutes'),
    ('02:00:00', '2 hours'),
    ('02:30:00', '2 and a half hours'),
    ('03:00:00', 'more than 2 and a half hours')
]

HEAR_CHOICE = [
    ("event", "event"),
    ("facebook", "facebook"),
    ("friends", "friends"),
    ("newspaper", "newspaper"),
    ("search", "search"),
    ("other", "other")
]