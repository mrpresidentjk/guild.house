# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import re
from .. import utils
from . import querysets, settings
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.db import models, IntegrityError
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from project import utils
from taggit.managers import TaggableManager


def get_current_site():
    try:
        return Site.objects.get_current().pk
    except Site.DoesNotExist:
        pass

@python_2_unicode_compatible
class Booking(models.Model):

    code = models.CharField(max_length=8, blank=True, default='')

    name = models.CharField(max_length=200)

    party_size = models.PositiveIntegerField()

    status = models.CharField(max_length=50, choices=settings.STATUS_CHOICES,
                              default=settings.STATUS_CHOICES[0][0])

    notes = models.TextField(blank=True, default='')

    email = models.EmailField(blank=True, default='')

    phone = models.CharField(max_length=100, blank=True, default='',
                             help_text="One phone number only. Put additional numbers in 'notes' if necessary."
    )

    booking_method = models.CharField(max_length=50, choices=settings.METHOD_CHOICE,
                                      default=settings.METHOD_CHOICE[0][0])

    user = models.ForeignKey(User, blank=True, null=True)

    site = models.ForeignKey('sites.Site', default=get_current_site,
                             related_name='bookings_booking',
                             on_delete=models.PROTECT)

    reserved_date = models.DateField(db_index=True, default=timezone.now)
    reserved_time = models.TimeField(db_index=True, default=timezone.now)

    service = models.CharField(max_length=50, choices=settings.SERVICE_CHOICE,
                               blank=True, default=''
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    updated_at = models.DateTimeField(auto_now=True, editable=False)

    objects = querysets.QuerySet.as_manager()

    class Meta(object):
        ordering = ['reserved_date', 'reserved_time', 'name']
        verbose_name_plural = 'bookings'

    def __str__(self):
        return self.name

    def clean(self, *args, **kwargs):
        if not self.email and not self.phone:
            raise ValidationError('Either a phone or an email address must be provided (or both).')
        return super(Booking, self).clean(*args, **kwargs)

    def get_absolute_url(self):


        return reverse('bookings:booking_day',
                       kwargs={'year': '%04d' % (self.reserved_date.year),
                               'month': '%02d' % (self.reserved_date.month),
                               'day': '%02d' % (self.reserved_date.day)})

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

    def save(self,*args, **kwargs):
        self.clean()

        # Automatically make code if doesn't already have one.
        if not self.code:
            self.code = utils.generate_unique_hex(queryset=Booking.objects.all())

        # Automatically set service based upon `reserved_time`.
        for i, t in enumerate(settings.SERVICE_TIMES):
            if self.reserved_time >= t[0]:
                service = settings.SERVICE_TIMES[i][1]
        self.service = service

        # Clean phone number
        self.phone = re.sub('[^0-9]','', self.phone)

        # Create a user whose username is email address if there is one, but
        # phone number if there is not.
        if not self.user:
            if self.email:
                email = username = self.email
                try:
                    user = User.objects.create_user(
                        username=username,
                        email=email
                    )
                    user.first_name = self.name
                    user.save()
                except IntegrityError:
                    user =  User.objects.get(username=username, email=email)
            elif self.phone:
                username = password = self.phone
                try:
                    user = User.objects.create_user(username=username)
                    user.first_name = self.name
                    user.save()
                except IntegrityError:
                    user = User.objects.get(username=username)
                    self.user = user

        super(Booking, self).save(*args, **kwargs)
