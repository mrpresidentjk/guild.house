# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import calendar
import datetime
from . import settings
from .forms import BookingForm
from .models import Booking
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Count, Sum
from django.shortcuts import redirect, get_object_or_404
from django.utils.timezone import localtime, now
from django.views import generic

class CalendarMixin(object):
    """ @TD: Fri Jun 24 11:46:48 AEST 2016: This is overkill, but was useful in a past
    time. Needs major clean up."""

    def get_calendar(self, context, yr=None, mth=None, day=None):

        if yr and mth:
            y = int(yr)
            m = int(mth)
        else:
            d = datetime.datetime.today()
            y = d.year
            m = d.month
            context['today'] = datetime.date(year=d.year, month=d.month, day=d.day)

        this_month = datetime.date(year=y, month=m, day=1)
        next_mth = this_month+relativedelta(months=+1)
        prev_mth = this_month+relativedelta(months=-1)
        context['cal_next_mth'] = '/%s/%02d/' % (next_mth.year, next_mth.month)
        context['cal_prev_mth'] = '/%s/%02d/' % (prev_mth.year, prev_mth.month)
        context['cal_next_yr'] = '/%s/%02d/' % (this_month.year+1, this_month.month)
        context['cal_prev_yr'] = '/%s/%02d/' % (this_month.year-1, this_month.month)
        context['month'] = this_month
        context['calendar'] = self.make_range(y,m)
        return context

    def make_range(self, y,m):
        c = calendar.monthrange(y, m)
        a = datetime.timedelta(days=c[0])
        b = datetime.timedelta(days=settings.DEFAULT_CALENDAR_LENGTH)

        # e = Booking.objects.filter(date__year=y, date__month=m)
        start = datetime.date.today()-\
                datetime.timedelta(datetime.date.today().weekday())
        end = start+b
        date_range = []
        while start<end:
            date_range.append({'day':start})
            # date_range.append({'day':start, 'events':e.filter(date=start)})
            start = start+datetime.timedelta(days=1)
        return date_range

    def get_context_data(self, *args, **kwargs):
        context = super(CalendarMixin, self).get_context_data(*args, **kwargs)
        context = self.get_calendar(context)
        context['tomorrow'] = date.today()+timedelta(days=1)
        return context


class BookingQueryset(object):

    model = Booking
    allow_future = True
    date_field = 'reserved_date'
    month_format = '%m'
    week_format = "%W"
    paginate_by = settings.BOOKINGS_PAGINATE_BY

    def get_context_data(self, *args, **kwargs):
        context = super(BookingQueryset, self).get_context_data(*args, **kwargs)
        context['future_list'] = self.get_queryset().future()
        context['summary_list'] = self.get_queryset().values('reserved_date')\
                                      .annotate(count=Count('id'),
                                                pax=Sum('party_size'))\
                                      .order_by('reserved_date')
        return context

    # def get_queryset(self, *args, **kwargs):
    #     queryset = super(BookingQueryset, self).get_queryset(*args, **kwargs)
    #     return queryset.active().future().order_by('reserved_date', 'reserved_time')


class BookingCreateView(CalendarMixin, BookingQueryset, generic.edit.CreateView):

    form_class = BookingForm

    def get_context_data(self, *args, **kwargs):
        context = super(BookingCreateView, self).get_context_data(*args, **kwargs)
        context = self.get_calendar(context)
        context['tomorrow'] = date.today()+timedelta(days=1)
        return context

    def get_initial(self):
        initial = super(BookingCreateView, self).get_initial()
        initial = initial.copy()
        # set as tomorrow if booking made later than 6pm
        if localtime(now()).hour > 18:
            initial['reserved_date'] = date.today()+timedelta(days=1)
        else:
            initial['reserved_date'] = date.today()
        initial['reserved_time'] = settings.DEFAULT_BOOKING_TIME
        return initial



class BookingUpdateView(CalendarMixin, BookingQueryset, generic.edit.UpdateView):

    slug_field = 'code'
    form_class = BookingForm

    def get_object(self):
        return get_object_or_404(Booking, code=self.kwargs.get('code'))

class BookingListView(BookingQueryset, generic.ListView):

    def get(self, *args, **kwargs):
        page = self.kwargs.get('page', None)
        if page is not None and int(page) < 2:
            return redirect('bookings:booking_list', permanent=True)
        return super(BookingListView, self).get(*args, **kwargs)


class BookingCancelledView(BookingQueryset, generic.ListView):

    template_name = 'bookings/booking_list_cancelled.html'

    def get_queryset(self, *args, **kwargs):
        # queryset = super(BookingCancelledView, self).get_queryset(*args, **kwargs)
        return Booking.objects.filter(status='Cancelled').order_by('-updated_at')


class BookingYearArchiveView(BookingQueryset, generic.YearArchiveView):

    make_object_list = True


class BookingMonthArchiveView(BookingQueryset, generic.MonthArchiveView):

    pass


class BookingDayArchiveView(BookingQueryset, generic.DayArchiveView):

    def get_context_data(self, *args, **kwargs):
        context_data = super(BookingDayArchiveView, self).get_context_data(*args,
                                                                      **kwargs)
        context_data['total'] = context_data['object_list'].aggregate(Sum('party_size'))
        context_data['cancelled_list'] = self.get_dated_queryset()\
                                             .filter(status='Cancelled')\
                                             .order_by('name')
        return context_data


class BookingTodayArchiveView(BookingQueryset, generic.TodayArchiveView):

    pass


class BookingWeekArchiveView(BookingQueryset, generic.WeekArchiveView):

    pass


class BookingDetailView(BookingQueryset, generic.DetailView):

    pass
