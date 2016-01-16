# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import settings
from .models import Homepage
from django.http import Http404
from django.views import generic


class HomepageDetailView(generic.DetailView):

    model = Homepage

    def get_categories(self):
        return self.object.site.library_categories.featured().active()[
            :settings.HOMEPAGE_CATEGORIES]

    def get_context_data(self, *args, **kwargs):
        context_data = super(HomepageDetailView, self).get_context_data(
            *args, **kwargs)
        context_data.update({'category_list': self.get_categories(),
                             'game_list': self.get_games()})
        return context_data

    def get_games(self):
        return self.object.site.library_games.featured().active()[
            :settings.HOMEPAGE_GAMES]

    def get_object(self, *args, **kwargs):
        try:
            return Homepage.objects.active().get_current()
        except Homepage.DoesNotExist:
            raise Http404('Homepage does not exist.')
