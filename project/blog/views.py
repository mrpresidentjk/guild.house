# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import settings
from .models import Entry
from django.shortcuts import redirect
from django.views import generic


class EntryDetailView(generic.DetailView):

    allow_future = True

    date_field = 'publish_at'

    model = Entry

    month_format = '%m'

    def get_queryset(self, *args, **kwargs):
        queryset = super(EntryDetailView, self).get_queryset(*args, **kwargs)
        return queryset.current_site().active()


class EntryListView(generic.ListView):

    model = Entry

    paginate_by = settings.ENTRIES_PAGINATE_BY

    def get(self, *args, **kwargs):
        page = self.kwargs.get('page', None)
        if page is not None and int(page) < 2:
            return redirect('blog:entry_list', permanent=True)
        return super(EntryListView, self).get(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        queryset = super(EntryListView, self).get_queryset(*args, **kwargs)
        return queryset.current_site().active()
