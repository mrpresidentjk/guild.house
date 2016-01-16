# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib.sites.models import Site
from django.db import models


class QuerySet(models.query.QuerySet):

    def active(self):
        return self.filter(is_enabled=True)

    def current_site(self):
        site = Site.objects.get_current()
        return self.filter(site=site)

    def featured(self):
        return self.filter(is_featured=True)
