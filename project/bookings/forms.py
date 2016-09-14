# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import re
from .models import Booking
from .settings import DURATION_SELECTION
from datetime import date, timedelta, datetime
from django import forms
from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django.forms.fields import CharField
from django.utils.encoding import force_text
from tinymce.widgets import TinyMCE


PHONE_DIGITS_RE = re.compile(r'^(\d{8})$|^([0-1]\d{9})$')


class AUPhoneNumberField(CharField):
    """
    A form field that validates input as an Australian phone number.
    Valid numbers have ten digits.
    """
    default_error_messages = {
        'invalid': 'Enter a valid phone number.'
    }

    def clean(self, value):
        """
        Validate a phone number. Strips parentheses, whitespace and hyphens.
        """
        super(AUPhoneNumberField, self).clean(value)
        if value in EMPTY_VALUES:
            return ''
        value = re.sub('(\(|\)|\s+|-)', '', force_text(value))
        phone_match = PHONE_DIGITS_RE.search(value)

        if phone_match:
            return '%s' % phone_match.group(1)
        raise ValidationError(self.error_messages['invalid'])


class BookingAdminForm(forms.ModelForm):

    class Meta(object):
        fields = ['name', 'site', 'reserved_date', 'reserved_time']
        model = Booking
        widgets = {'notes': TinyMCE()}


class BookingForm(forms.ModelForm):
    required_css_class = 'required'
    booking_duration = forms.ChoiceField(widget=forms.Select(),
                                         choices=DURATION_SELECTION)
    phone = AUPhoneNumberField(widget=forms.TextInput(attrs={'placeholder': '**'}))


    class Meta(object):
        fields = ['status', 'name', 'reserved_time', 'reserved_date',
                  'booking_duration', 'party_size', 'area', 'email', 'phone',
                  'postcode', 'notes','user', 'updated_by', 'hear_choices',
                  'hear_other', 'booking_method', 'private_notes', 'busy_night']
        model = Booking
        widgets = {
            'notes': forms.Textarea(attrs={'rows':4,  'width':185, 'cols':0}),
            'email': forms.TextInput(attrs={'placeholder': '**', }),
            'name': forms.TextInput(attrs={'placeholder': '**'}),
            'party_size': forms.TextInput(attrs={'placeholder': '**'}),
            'hear_other': forms.Textarea(attrs={'rows':4,  'width':185, 'cols':0}),
        }

    def __init__(self, user=None, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['phone'].required = True
        self.fields['email'].required = True
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['updated_by'].widget = forms.HiddenInput()

    def clean(self, *args, **kwargs):
        cleaned_data = super(BookingForm, self).clean(*args, **kwargs)
        if not cleaned_data.get('email') and not cleaned_data.get('phone'):
            raise forms.ValidationError('Both a phone number and an email address are necessary for online bookings.')
        return super(BookingForm, self).clean(*args, **kwargs)


class NewBookingForm(BookingForm):

    def __init__(self, user=None, *args, **kwargs):
        super(NewBookingForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget = forms.HiddenInput()
        self.fields['private_notes'].widget = forms.HiddenInput()
        self.fields['busy_night'].widget = forms.HiddenInput()
        if not user.is_authenticated():
            self.fields['booking_method'].widget = forms.HiddenInput()
