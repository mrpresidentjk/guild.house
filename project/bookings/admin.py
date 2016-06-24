# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .forms import BookingAdminForm
from .models import Booking
from django.contrib import admin


def get_obj_link(obj):
    return "<a href='{0}'>{1}</a>".format(obj.get_absolute_url(), obj.code)
get_obj_link.allow_tags = True
get_obj_link.short_description = "URL"

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    date_hierarchy = 'reserved_date'

    fieldsets = [
        ('Content', {'fields': ['reserved_date', 'reserved_time', 'name', 'party_size', 'status', 'email',
                                'phone']}),
        ('Publishing', {'fields': ['site', ('created_at', 'updated_at')],
                        'classes': ['collapse']}),
    ]

    form = BookingAdminForm

    list_display = ['name', 'reserved_date', 'reserved_time', 'party_size', 'status', 'phone', 'email', get_obj_link]

    list_filter = ['reserved_date', 'reserved_time', 'status']

    #prepopulated_fields = {'slug': ['name']}

    readonly_fields = ['created_at', 'updated_at']

    search_fields = ['name', 'email', 'notes', 'reserved_date']
