# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .models import Homepage
from django.http import Http404
from django.views import generic


class HomepageDetailView(generic.DetailView):

    model = Homepage

    def get_object(self, *args, **kwargs):
        try:
            return Homepage.objects.active().get_current()
        except Homepage.DoesNotExist:
            raise Http404('Homepage does not exist.')
