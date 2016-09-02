# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .models import Booking
from .settings import DURATION_SELECTION
from datetime import date, timedelta
from django import forms
from tinymce.widgets import TinyMCE


class BookingAdminForm(forms.ModelForm):

    class Meta(object):
        fields = ['name', 'site', 'reserved_date', 'reserved_time']
        model = Booking
        widgets = {'notes': TinyMCE()}


class BookingForm(forms.ModelForm):
    required_css_class = 'required'
    booking_duration = forms.ChoiceField(widget=forms.Select(),
                                         choices=DURATION_SELECTION)


    class Meta(object):
        fields = ['name', 'reserved_time', 'reserved_date', 'booking_duration',
                  'party_size', 'email', 'phone', 'booking_method', 'status',
                  'notes']
        model = Booking
        widgets = {
            'notes': forms.Textarea(attrs={'rows':4,  'width':185, 'cols':0}),
            'email': forms.TextInput(attrs={'placeholder': '**', }),
            'phone': forms.TextInput(attrs={'placeholder': '**'}),
            'name': forms.TextInput(attrs={'placeholder': '**'}),
            'party_size': forms.TextInput(attrs={'placeholder': '**'}),
        }

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['phone'].required = True
        self.fields['email'].required = True

    def clean(self, *args, **kwargs):
        cleaned_data = super(BookingForm, self).clean(*args, **kwargs)
        if not cleaned_data.get('email') and not cleaned_data.get('phone'):
            raise forms.ValidationError('Both a phone number and an email address are necessary for online bookings.')
        return super(BookingForm, self).clean(*args, **kwargs)


class NewBookingForm(BookingForm):

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['booking_method'].widget = forms.HiddenInput()
        self.fields['status'].widget = forms.HiddenInput()


# Have to be logged in to make changes to booking.
#