# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib.sites.models import Site
from django.db import models
from django.utils import timezone


class QuerySet(models.query.QuerySet):

    def active(self):
        return self.current_site().exclude(status="Cancelled")

    def current_site(self):
        site = Site.objects.get_current()
        return self.filter(site=site)

    def past(self):
        now = timezone.now()
        return self.filter(reserved_for__lte=now)

    def future(self):
        now = timezone.now()
        return self.filter(reserved_for__gt=now)
