# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .models import Event, EventUser
from django import forms
from tinymce.widgets import TinyMCE


class EventAdminForm(forms.ModelForm):

    class Meta(object):
        exclude = []
        model = Event
        widgets = {'content': TinyMCE()}


class EventUserForm(forms.ModelForm):
    model = EventUser