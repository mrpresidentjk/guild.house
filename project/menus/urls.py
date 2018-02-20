# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import feeds, views
from django.conf.urls import include, url


urls = [

    url(r'^$', views.MenuTypeListView.as_view(), name='menutype_list'),

    url(r'^(?P<page>\d+)$', views.MenuTypeListView.as_view(), name='menutype_list'),

    url(r'^latest\.xml$', feeds.MenuFeed(), name='menu_feed'),
]

urlpatterns = [url(r'^', include(urls, namespace='menus'))]
