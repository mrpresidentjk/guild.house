# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .models import Homepage
from django.contrib.sitemaps import Sitemap


class HomepageSitemap(Sitemap):

    def items(self):
        return Homepage.objects.current_site().active()

    def lastmod(self, obj):
        return obj.updated_at


sitemaps = {'site_homepage': HomepageSitemap}
