# -*- coding: utf-8 -*-
from django import forms

from project.fields import AUPhoneNumberField
from project.rolodex.models import Email, Phone

from . import settings
from .models import TemporaryMember


class TemporaryMemberForm(forms.Form):

    surname = forms.CharField()
    first_name = forms.CharField()
    email = forms.EmailField()
    phone = AUPhoneNumberField()
    # widget=forms.TextInput())  # attrs={'placeholder': '**'}))
    address = forms.CharField(widget=forms.Textarea)
    suburb = forms.CharField()
    postcode = forms.CharField()
    state = forms.CharField(initial="ACT")
    country = forms.CharField(initial="Australia")
    dob = forms.DateField(label="Birth date")
    payment_method = forms.ChoiceField(
        choices=[('', '---')] + settings.PAYMENT_METHODS)  # .insert(0, ))
    survey_games = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label="What's your favourite game?",
        help_text="List as many as you like.")
    survey_food = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label="What food, drink or pizza would you like see on our menu?",  # noqa
        help_text="Say as much as you want.")
    survey_hear = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label="How did you hear about us?",
        help_text="Tell us a story.")
    survey_suggestions = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label="Any suggestions you would have for us?",
        help_text="We're still pretty new and learning as we go!")

    class Meta:
        model = TemporaryMember
        exclude = ['is_checked', 'is_approved_paid', 'notes',
                   'approved_by', 'approved_payment_method']
