# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib import admin
from django.contrib.flatpages.admin import FlatpageForm, FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE


class PageForm(FlatpageForm):

    class Meta:
        exclude = []
        model = FlatPage
        widgets = {'content': TinyMCE()}


class PageAdmin(FlatPageAdmin):
    form = PageForm

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, PageAdmin)