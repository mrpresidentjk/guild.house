# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import querysets, settings
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from project import utils
from taggit.managers import TaggableManager


def get_current_site():
    try:
        return Site.objects.get_current().pk
    except Site.DoesNotExist:
        pass

STATUS_CHOICES = [
    ('Confirmed', 'Confirmed'),
    ('Unconfirmed', 'Unconfirmed'),
    ('Numbers Unconfirmed', 'Numbers Unconfirmed'),
    ('Big Booking', 'Big Booking'),
    ('Cancelled', 'Cancelled'),
]


@python_2_unicode_compatible
class Booking(models.Model):

    name = models.CharField(max_length=200)

    party_size = models.PositiveIntegerField()

    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    notes = models.TextField(blank=True, default='')

    email = models.EmailField(blank=True, default='')

    phone = models.CharField(max_length=100, blank=True, default='')

    user = models.ForeignKey(User, blank=True, null=True)

    site = models.ForeignKey('sites.Site', default=get_current_site,
                             related_name='bookings_booking',
                             on_delete=models.PROTECT)

    reserved_for = models.DateTimeField(db_index=True, default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    updated_at = models.DateTimeField(auto_now=True, editable=False)

    objects = querysets.QuerySet.as_manager()

    class Meta(object):
        ordering = ['-reserved_for', 'name']
        unique_together = ['site', 'reserved_for', 'phone']
        verbose_name_plural = 'bookings'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        server_timezone = timezone.pytz.timezone(settings.TIME_ZONE)

        if timezone.is_naive(self.reserved_for):
            reserved_for = server_timezone.localize(self.reserved_for)
        else:
            reserved_for = server_timezone.normalize(self.reserved_for)

        return reverse('bookings:booking_detail',
                       kwargs={'year': '%04d' % (reserved_for.year),
                               'month': '%02d' % (reserved_for.month),
                               'slug': self.slug})

    def get_next(self):
        queryset = self.__class__.objects.exclude(pk=self.pk).filter(
            site=self.site, reserved_for__gte=self.reserved_for
            ).active().order_by('reserved_for')
        return queryset.first()

    def get_previous(self):
        queryset = self.__class__.objects.exclude(pk=self.pk).filter(
            site=self.site, reserved_for__lte=self.reserved_for
            ).active().order_by('-reserved_for')
        return queryset.first()

    def is_active(self):
        return self in self.__class__.objects.filter(pk=self.pk).active()
    is_active.boolean = True
    is_active.short_description = 'active'
