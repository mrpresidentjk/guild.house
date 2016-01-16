# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .models import Entry
from django import forms
from tinymce.widgets import TinyMCE


class EntryAdminForm(forms.ModelForm):

    class Meta(object):
        fields = ['title', 'heading', 'summary', 'featured_content', 'content',
                  'meta_description', 'is_enabled', 'is_featured', 'site',
                  'slug', 'publish_at', 'tags']
        model = Entry
        widgets = {'content': TinyMCE()}
