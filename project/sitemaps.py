# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib.flatpages.sitemaps import FlatPageSitemap as flatpages
from project.blog.sitemaps import sitemaps as blog
from project.library.sitemaps import sitemaps as library
from project.site.sitemaps import sitemaps as site


sitemaps = {}
sitemaps['flatpages'] = flatpages
sitemaps.update(blog)
sitemaps.update(site)
