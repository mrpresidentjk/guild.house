# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from . import settings
from .models import Booking
from django.shortcuts import redirect
from django.views import generic


class BookingQueryset(object):

    model = Booking
    allow_future = True
    date_field = 'reserved_for'
    month_format = '%m'

    def get_context_data(self, *args, **kwargs):
        context = super(BookingQueryset, self).get_context_data(*args, **kwargs)
        context['future_bookings_list'] = self.get_queryset().future()
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super(BookingQueryset, self).get_queryset(*args, **kwargs)
        return queryset.active()


class BookingCreateView(BookingQueryset, generic.edit.CreateView):

    fields = ['reserved_for', 'name', 'party_size', 'email', 'phone']


class BookingListView(BookingQueryset, generic.ListView):

    model = Booking

    paginate_by = settings.BOOKINGS_PAGINATE_BY

    def get(self, *args, **kwargs):
        page = self.kwargs.get('page', None)
        if page is not None and int(page) < 2:
            return redirect('bookings:booking_list', permanent=True)
        return super(BookingListView, self).get(*args, **kwargs)


class BookingYearArchiveView(BookingQueryset, generic.YearArchiveView):

    make_object_list = True


class BookingMonthArchiveView(BookingQueryset, generic.MonthArchiveView):

    pass


class BookingDayArchiveView(BookingQueryset, generic.DayArchiveView):

    pass


class BookingTodayArchiveView(BookingQueryset, generic.DayArchiveView):

    pass


class BookingWeekArchiveView(BookingQueryset, generic.WeekArchiveView):

    week_format = "%W"


class BookingDetailView(BookingQueryset, generic.DetailView):

    pass
