# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import feeds, views
from django.conf.urls import include, url


urls = [

    url(r'^$', views.EntryListView.as_view(), name='entry_list'),

    url(r'^(?P<page>\d+)$', views.EntryListView.as_view(), name='entry_list'),

    url(r'^latest\.xml$', feeds.EntryFeed(), name='entry_feed'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[\w-]+)$',
        views.EntryDetailView.as_view(), name='entry_detail'),

]

urlpatterns = [url(r'^', include(urls, namespace='blog'))]
