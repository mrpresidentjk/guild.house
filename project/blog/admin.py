# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .forms import EntryAdminForm
from .models import Entry
from django.contrib import admin


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):

    date_hierarchy = 'publish_at'

    fieldsets = [
        ('Content', {'fields': ['title', 'heading', 'summary',
                                'featured_content', 'content',
                                'meta_description']}),
        ('Publishing', {'fields': ['is_enabled', 'is_featured', 'site', 'slug',
                                   'publish_at', 'tags',
                                   ('created_at', 'updated_at')],
                        'classes': ['collapse']}),
    ]

    form = EntryAdminForm

    list_display = ['title', 'publish_at', 'is_active', 'is_featured']

    list_filter = ['is_enabled', 'is_featured']

    prepopulated_fields = {'slug': ['title']}

    readonly_fields = ['created_at', 'updated_at']

    search_fields = ['title']
