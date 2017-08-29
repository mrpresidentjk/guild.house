# -*- coding: utf-8 -*-
from django.conf.urls import include, url

from . import views


urls = [

    url(r'^new/',
        views.MemberCreateView.as_view(),
        name='member_form'),

]

urlpatterns = [url(r'^', include(urls, namespace='members'))]
