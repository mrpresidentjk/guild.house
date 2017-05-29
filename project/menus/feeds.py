# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import settings
from .models import MenuType
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed


class MenuFeed(Feed):

    feed_type = Atom1Feed

    model = MenuType

    subtitle = 'Current menus.'

    def link(self):
        return reverse('menus:menu_list')

    def title(self):
        site = Site.objects.get_current()
        return '{0} - Menus'.format(site.name)

    def items(self):
        return self.model.objects.current_site().current()

    def item_title(self, item):
        return '{0}'.format(item)

    def item_description(self, item):
        return item.summary

    def item_pubdate(self, item):
        return item.publish_at
