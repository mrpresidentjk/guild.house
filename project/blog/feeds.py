# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import settings
from .models import Entry
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed


class EntryFeed(Feed):

    feed_type = Atom1Feed

    model = Entry

    subtitle = 'Latest blog entries.'

    def link(self):
        return reverse('blog:entry_list')

    def title(self):
        site = Site.objects.get_current()
        return '{0} - Blog'.format(site.name)

    def items(self):
        return self.model.objects.current_site().active().order_by(
            '-publish_at')[:settings.ENTRIES_FEED]

    def item_title(self, item):
        return '{0}'.format(item)

    def item_description(self, item):
        return item.summary

    def item_pubdate(self, item):
        return item.publish_at
