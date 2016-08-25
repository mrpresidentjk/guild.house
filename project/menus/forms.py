# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .models import MenuType
from django import forms
from tinymce.widgets import TinyMCE


class MenuTypeAdminForm(forms.ModelForm):

    class Meta(object):
        fields = ['is_enabled', 'title', 'summary', 'menu_image', 'menu_file', ]
        model = MenuType
        widgets = {'summary': TinyMCE()}
