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

DEFAULT_BOOKING_METHOD = getattr(settings, 'BOOKINGS_DEFAULT_BOOKING_METHOD',
                                 'website')
METHOD_CHOICE = [
    ('phone', 'Phone'),
    ('email', 'Email'),
    ('website', 'Online'),
    ('facebook', 'Facebook Messenger'),
    ('person', 'In Person'),
    ('other', 'Other'),
]

SERVICE_CHOICE = (
    ('lunch', 'Lunch'),
    ('afternoon', 'Afternoon'),
    ('main', 'Main'),
)

SERVICE_TIMES = (
    (time(12,0), 'lunch'),
    (time(14,30), 'afternoon'),
    (time(17,30), 'main'),
)

BOOKING_TIMES = (time(12), time(23))
BOOKING_INTERVAL = timedelta(minutes=30)

DEFAULT_BOOKING_DURATION = getattr(settings, 'BOOKINGS_DEFAULT_BOOKING_DURATION',
                                   '2:30:00')

DURATION_SELECTION = [
    ('0:15:00', '15 minutes'),
    ('0:30:00', '30 minutes'),
    ('0:45:00', '45 minutes'),
    ('1:00:00', '1 hour'),
    ('1:15:00', '1 hour and 15 minutes'),
    ('1:30:00', '1 and a half hours'),
    ('1:45:00', '1 hour and 45 minutes'),
    ('2:00:00', '2 hours'),
    ('2:30:00', '2 and a half hours'),
    ('3:00:00', 'more than 2 and a half hours')
]

HEAT = {
    65: 'warm',
    85: 'hot',
    105: 'full',
}

HEAR_CHOICE = [
    ("event", "event"),
    ("facebook", "facebook"),
    ("friends", "friends"),
    ("newspaper", "newspaper"),
    ("search", "search"),
    ("other", "other")
]