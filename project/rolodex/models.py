# -*- coding: utf-8 -*-
from django.db import models


class AbstractRolodex(models.Model):

    is_working = models.BooleanField(default=True)

    created_at = models.DateField(auto_now_add=True)

    last_checked_at = models.DateTimeField(auto_now=True,
                                           editable=True)

    class Meta:
        abstract = True


class Email(AbstractRolodex, models.Model):

    email = models.EmailField()

    def __str__(self):
        return self.email


class Phone(AbstractRolodex, models.Model):

    phone = models.CharField(max_length=16)

    def __str__(self):
        return self.phone
