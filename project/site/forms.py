# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .models import Homepage
from django import forms
from tinymce.widgets import TinyMCE


class HomepageAdminForm(forms.ModelForm):

    class Meta(object):
        fields = ['title', 'heading', 'featured_content', 'content',
                  'meta_description', 'site', 'is_enabled']
        model = Homepage
        widgets = {'content': TinyMCE()}
