# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib.sites.models import Site
from django.db import models
from django.utils import timezone


class QuerySet(models.query.QuerySet):

    def active(self):
        return self.filter(is_enabled=True).published()

    def current_site(self):
        site = Site.objects.get_current()
        return self.filter(site=site)

    def featured(self):
        return self.filter(is_featured=True)

    def published(self):
        now = timezone.now()
        return self.filter(publish_at__lte=now)

    def unpublished(self):
        now = timezone.now()
        return self.filter(publish_at__gt=now)
