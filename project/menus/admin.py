# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .forms import MenuTypeAdminForm
from .models import MenuType
from django.contrib import admin


@admin.register(MenuType)
class MenuTypeAdmin(admin.ModelAdmin):

    form = MenuTypeAdminForm

    list_display = ['title', 'order',  'updated_at']
    list_editable = ['order']