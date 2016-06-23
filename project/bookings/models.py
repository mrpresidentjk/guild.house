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


METHOD_CHOICE = [
    ('phone', 'Phone'),
    ('email', 'Email'),
    ('facebook', 'Facebook'),
    ('person', 'In Person'),
    ('other', 'Other'),
]


@python_2_unicode_compatible
class Booking(models.Model):

    name = models.CharField(max_length=200)

    party_size = models.PositiveIntegerField()

    status = models.CharField(max_length=50, choices=STATUS_CHOICES,
                              default=STATUS_CHOICES[0][0])

    notes = models.TextField(blank=True, default='')

    email = models.EmailField(blank=True, default='')

    phone = models.CharField(max_length=100, blank=True, default='')

    booking_method = models.CharField(max_length=50, choices=METHOD_CHOICE,
                                      default=METHOD_CHOICE[0][0])

    user = models.ForeignKey(User, blank=True, null=True)

    site = models.ForeignKey('sites.Site', default=get_current_site,
                             related_name='bookings_booking',
                             on_delete=models.PROTECT)

    reserved_date = models.DateField(db_index=True, default=timezone.now)
    reserved_time = models.TimeField(db_index=True, default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    updated_at = models.DateTimeField(auto_now=True, editable=False)

    objects = querysets.QuerySet.as_manager()

    class Meta(object):
        ordering = ['-reserved_date', 'reserved_time', 'name']
        unique_together = ['site', 'reserved_date', 'reserved_time', 'phone']
        verbose_name_plural = 'bookings'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        server_timezone = timezone.pytz.timezone(settings.TIME_ZONE)

        if timezone.is_naive(self.reserved_date):
            reserved_date = server_timezone.localize(self.reserved_date)
        else:
            reserved_date = server_timezone.normalize(self.reserved_date)

        return reverse('bookings:booking_detail',
                       kwargs={'year': '%04d' % (reserved_date.year),
                               'month': '%02d' % (reserved_date.month),
                               'slug': self.slug})

    def get_next(self):
        queryset = self.__class__.objects.exclude(pk=self.pk).filter(
            site=self.site, reserved_date__gte=self.reserved_date
            ).active().order_by('reserved_date', 'reserved_time')
        return queryset.first()

    def get_previous(self):
        queryset = self.__class__.objects.exclude(pk=self.pk).filter(
            site=self.site, reserved_date__lte=self.reserved_date
            ).active().order_by('-reserved_date', 'reserved_time')
        return queryset.first()

    def is_active(self):
        return self in self.__class__.objects.filter(pk=self.pk).active()
    is_active.boolean = True
    is_active.short_description = 'active'
