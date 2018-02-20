# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import settings
from .models import Menu
from django.contrib.sitemaps import Sitemap
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse


class MenuSitemap(Sitemap):

    model = Menu

    def items(self):
        return self.model.objects.current_site().indexable()

    def lastmod(self, obj):
        return obj.updated_at


class MenuListSitemap(Sitemap):

    model = Menu

    def items(self):
        objects = self.model.objects.current_site().current()
        page_size = settings.ENTRIES_PAGINATE_BY
        return Paginator(objects, page_size).page_range if page_size else [1]

    def location(self, page):
        if page == 1:
            return reverse('menus:menu_list')
        else:
            return reverse('menus:menu_list', kwargs={'page': page})


sitemaps = {'menus_menu': MenuSitemap,
            'menus_menulist': MenuListSitemap}
