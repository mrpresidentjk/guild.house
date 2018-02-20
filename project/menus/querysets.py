# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib.sites.models import Site
from django.db import models


class QuerySet(models.query.QuerySet):

    def current_site(self):
        site = Site.objects.get_current()
        return self.filter(site=site)

    def current(self):
        return self.filter(is_current=True)
