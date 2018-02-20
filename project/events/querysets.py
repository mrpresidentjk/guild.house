# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib.sites.models import Site
from django.db import models
from django.utils import timezone


class QuerySet(models.query.QuerySet):

    def active(self):
        return self.filter(is_enabled=True).published()

    def featured(self):
        return self.filter(spotlight=True)

    def published(self):
        now = timezone.now()
        if self.expires:
            return self.filter(expires__gt=now)
        return self
