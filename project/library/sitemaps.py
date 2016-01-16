# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .models import Category, Game
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse


class ViewSitemap(Sitemap):

    def items(self):
        return ['library:category_list']

    def location(self, item):
        return reverse(item)


class CategorySitemap(Sitemap):

    def items(self):
        return Category.objects.current_site().active()

    def lastmod(self, obj):
        return obj.updated_at


class GameSitemap(Sitemap):

    def items(self):
        return Game.objects.current_site().active()

    def lastmod(self, obj):
        return obj.updated_at


sitemaps = {'library': ViewSitemap,
            'library_category': CategorySitemap,
            'library_game': GameSitemap}
