# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import settings
from .models import Entry
from django.contrib.sitemaps import Sitemap
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse


class EntrySitemap(Sitemap):

    model = Entry

    def items(self):
        return self.model.objects.current_site().active()

    def lastmod(self, obj):
        return obj.updated_at


class EntryListSitemap(Sitemap):

    model = Entry

    def items(self):
        objects = self.model.objects.current_site().active()
        page_size = settings.ENTRIES_PAGINATE_BY
        return Paginator(objects, page_size).page_range if page_size else [1]

    def location(self, page):
        if page == 1:
            return reverse('blog:entry_list')
        else:
            return reverse('blog:entry_list', kwargs={'page': page})


sitemaps = {'blog_entry': EntrySitemap,
            'blog_entrylist': EntryListSitemap}
