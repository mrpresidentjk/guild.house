# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .models import Booking
from django import forms
from tinymce.widgets import TinyMCE


class BookingAdminForm(forms.ModelForm):

    class Meta(object):
        fields = ['name', 'site', 'reserved_for']
        model = Booking
        widgets = {'content': TinyMCE()}
