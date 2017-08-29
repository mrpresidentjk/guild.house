# -*- coding: utf-8 -*-
from django import forms

from project.fields import AUPhoneNumberField
from .models import TemporaryMember


class TemporaryMemberForm(forms.ModelForm):

    email = forms.EmailField()
    phone = AUPhoneNumberField(
        widget=forms.TextInput())  # attrs={'placeholder': '**'}))

    class Meta:
        model = TemporaryMember
        exclude = ['is_checked', 'is_approved_paid', 'notes',
                   'approved_by', 'approved_payment_method']
