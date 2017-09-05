# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib.auth.decorators import permission_required

from . import views


urls = [

    url(r'^new/',
        views.member_create_view,
        name='member_form'),

    url(r'^success/',
        views.TemporaryMemberSuccessView.as_view(),
        name='temporarymember_success_view'),

    url(r'^approve/',
        permission_required('members.can_change_member')(
            views.member_approval_view,
        ),
        name='member_approval'),
]

urlpatterns = [url(r'^', include(urls, namespace='members'))]
