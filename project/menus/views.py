# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import settings
from .models import MenuType
from django.shortcuts import redirect
from django.views import generic


class MenuTypeListView(generic.ListView):

    model = MenuType

    paginate_by = settings.ENTRIES_PAGINATE_BY

    def get(self, *args, **kwargs):
        page = self.kwargs.get('page', None)
        if page is not None and int(page) < 2:
            return redirect('menus:menu_list', permanent=True)
        return super(MenuTypeListView, self).get(*args, **kwargs)

    # def get_queryset(self, *args, **kwargs):
    #     queryset = super(MenuTypeListView, self).get_queryset(*args, **kwargs)
    #     return queryset.current_site().current()
