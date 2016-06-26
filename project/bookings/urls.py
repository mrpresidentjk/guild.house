# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import views
from django.conf.urls import include, url


urls = [

    url(r'^$',
        views.BookingListView.as_view(),
        name='booking_list'),

    url(r'^(?P<page>\d+)$', views.BookingListView.as_view(), name='booking_list'),

    url(r'^new/$',
        views.BookingCreateView.as_view(),
        name="booking_add"),

    url(r'^cancelled/$',
        views.BookingCancelledView.as_view(),
        name="booking_list_cancelled"),

    url(r'^today/$',
        views.BookingTodayArchiveView.as_view(),
        name="booking_today"),

    url(r'^(?P<year>\d{4})/$',
        views.BookingYearArchiveView.as_view(),
        name="booking_year"),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        views.BookingMonthArchiveView.as_view(),
        name="booking_month"),

    url(r'^(?P<year>\d{4})/week/(?P<week>\d+)/$',
        views.BookingWeekArchiveView.as_view(),
        name="booking_week"),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        views.BookingDayArchiveView.as_view(),
        name="booking_day"),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[\w-]+)$',
        views.BookingDetailView.as_view(),
        name='booking_detail'),

    url(r'^(?P<code>[\w-]+)/$',
        views.BookingUpdateView.as_view(),
        name="booking_update"),
]

urlpatterns = [url(r'^', include(urls, namespace='bookings'))]