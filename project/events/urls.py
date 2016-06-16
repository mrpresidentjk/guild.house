# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import views
from django.conf.urls import include, url, patterns


urls = [

    url(r'^$', views.EventListView.as_view(), name='event_list'),

    url(r'^(?P<page>\d+)$', views.EventListView.as_view(), name='event_list'),

    url(r"^regular/(?P<id>.*)/(?P<slug>.*)/$",
        views.event_recur, name="event_recur"),


    url(r"^(?P<slug>.*)/$",
        views.EventTicketView.as_view(), name="event_ticket"),


    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[\w-]+)$',
        views.EventDetailView.as_view(), name='event_detail'),

]

urlpatterns = [url(r'^', include(urls, namespace='events'))]
