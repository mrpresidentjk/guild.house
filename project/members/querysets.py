# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.db import models
from django.utils import timezone


class MemberQuerySet(models.query.QuerySet):

    def active(self):
        return self.filter(is_active=True)


class MembershipQuerySet(models.query.QuerySet):

    def active(self):
        return self.filter(valid_until__gte=timezone.now())

    def inactive(self):
        return self.filter(valid_until__lt=timezone.now())
