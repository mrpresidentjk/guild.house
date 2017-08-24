# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from .settings import BIG_BOOKING


class QuerySet(models.query.QuerySet):

    def active(self):
        return self.current_site().exclude(status="Cancelled")

    def big(self):
        return self.active().filter(party_size__gte=BIG_BOOKING)

    def current_site(self):
        site = Site.objects.get_current()
        return self.filter(site=site)

    def today_all(self):
        now = timezone.now()
        return self.filter(reserved_date=now)

    def today(self):
        return self.today_all().active()

    def past_all(self):
        now = timezone.now()
        return self.filter(reserved_date__lte=now)

    def past(self):
        return self.past_all().active()

    def future_all(self):
        now = timezone.now()
        return self.filter(reserved_date__gte=now)

    def future(self):
        return self.future_all().active()

    def future_by_date(self):
        now = timezone.now()
        return self.filter(reserved_date__gte=now)
