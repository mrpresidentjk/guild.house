# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import calendar
import datetime
from datetime import time, timedelta, date
from dateutil.relativedelta import relativedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Count, Sum
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.timezone import localtime, now
from django.views import generic
from django.conf import settings

from . import settings
from .forms import BookingForm, NewBookingForm, BlankForm
from .models import Booking, BookingDate
from .utils import import_revel_bookings, get_future_services_set

from django_weasyprint import WeasyTemplateResponseMixin



class CalendarMixin(object):
    """ @TD: Fri Jun 24 11:46:48 AEST 2016: This is overkill, but was useful in a past
    time. Needs major clean up."""

    def get_calendar(self, context, yr=None, mth=None, day=None):

        if yr and mth and day:
            y = int(yr)
            m = int(mth)
            d = int(day)
        else:
            today = datetime.datetime.today()
            y = today.year
            m = today.month
            d = today.day

        context['today'] = datetime.date(year=y, month=m, day=d)

        this_month = datetime.date(year=y, month=m, day=1)
        next_mth = this_month + relativedelta(months=+1)
        prev_mth = this_month + relativedelta(months=-1)
        context['cal_next_mth'] = '/%s/%02d/' % (next_mth.year, next_mth.month)
        context['cal_prev_mth'] = '/%s/%02d/' % (prev_mth.year, prev_mth.month)
        context['cal_next_yr'] = '/%s/%02d/' % (
            this_month.year + 1, this_month.month)
        context['cal_prev_yr'] = '/%s/%02d/' % (
            this_month.year - 1, this_month.month)
        context['month'] = this_month
        context['calendar'] = self.make_range(y, m, d)
        return context

    def make_range(self, y, m, d):
        c = calendar.monthrange(y, m)
        a = datetime.timedelta(days=c[0])
        b = datetime.timedelta(days=settings.DEFAULT_CALENDAR_LENGTH)

        # e = Booking.objects.filter(date__year=y, date__month=m)
        start = datetime.date(year=y, month=m, day=d) -\
            datetime.timedelta(datetime.date(year=y, month=m, day=d).weekday())
        end = start + b
        date_range = []
        while start < end:
            date_range.append({'day': start})
            # date_range.append({'day':start, 'events':e.filter(date=start)})
            start = start + datetime.timedelta(days=1)
        return date_range

    def get_context_data(self, *args, **kwargs):
        context = super(CalendarMixin, self).get_context_data(*args, **kwargs)
        context = self.get_calendar(context)
        context['tomorrow'] = context['today'] + timedelta(days=1)
        return context


class TimeMixin(object):

    def get_booking_list(self, this_date):
        return Booking.objects.filter(reserved_date=this_date)

    def generate_time_dict(self, this_date):
        """requires `this_date` as :py:class:`datetime.date`

        This is used to fetch bookings and to `datetime.combine` with
        `datetime.time` to create the necessary range of times.
        """
        busy_night = False
        open_bookings, time_list = [], []
        interval = settings.BOOKING_INTERVAL
        this_time = datetime.datetime.combine(this_date,
                                              settings.BOOKING_TIMES[0]) - interval

        """Construct bookings
        Ensure times are constructed first, then iterate through bookings
        for this day as likely the number of bookings will be fewer than the
        number of intervals. """

        booking_list = self.get_booking_list(this_date)
        for booking in booking_list:
            start_time = datetime.datetime.combine(
                this_date, booking.reserved_time)
            if booking.booking_duration:
                end_time = start_time + booking.booking_duration
            else:
                h, m = settings.DEFAULT_BOOKING_DURATION.split(":")[0]
                end_time = datetime.datetime.combine(
                    this_date,
                    time(hour=int(h), minute=int(m))
                )
            open_bookings.append((start_time, end_time, booking.party_size))

        select_time = datetime.datetime.combine(datetime.date(2000, 1, 1),
                                                settings.BOOKING_TIMES[0])
        while this_time <= datetime.datetime.combine(
                this_date,
                settings.BOOKING_TIMES[1]) - interval:
            this_time = this_time + interval
            this_dict = {'pax': 0,
                         'date': this_time,
                         'select_time': time(this_time.hour, this_time.minute),
                         'time': "{}:{:0>2}".format(this_time.hour,
                                                    this_time.minute)}

            # Add `party_size` totals to data_dict
            select_time = select_time + interval
            for start, end, pax in open_bookings:
                # Add an hour for good luck.
                if start <= this_time and this_time < end + timedelta(minutes=60):
                    this_dict['pax'] = this_dict['pax'] + pax

            for tmp in settings.HEAT.keys():
                if this_dict['pax'] < tmp:
                    break
                else:
                    this_dict['heat'] = settings.HEAT[tmp]

            # @@TODO get value from settings.HEAT
            if this_dict['pax'] > settings.VENUE_FULL:
                busy_night = True

            # Add `service` to dictionary
            for service_time, service in settings.SERVICE_TIMES:
                if time(this_time.hour, this_time.minute) == service_time:
                    this_dict['service'] = service
            time_list.append(this_dict)
        return time_list, busy_night

    def get_time_list(self, context, this_date):
        context['time_list'], context['busy_night'] = self.generate_time_dict(
            this_date)
        context['date'] = this_date
        context['booking_list'] = self.get_booking_list(this_date)

        # Sadly annotate too unreliable https://code.djangoproject.com/ticket/10060
        total_pax = 0
        for booking in self.get_booking_list(this_date):
            total_pax = total_pax + booking.party_size
        context['pax_total'] = total_pax
        return context


class BookingFormMixin(object):

    def get_object(self):
        return get_object_or_404(Booking, code=self.kwargs.get('code'))

    def send_booking_notice_internal(self, obj, form, change="added"):
        warning = ""
        if "full" in form.cleaned_data.get('private_notes'):
            warning = """Beware! This booking made during a busy time. May conflict. Please check ASAP and contact to discuss options if necessary.

The customer has been warned that this is the case and may be expecting confirmation.

        """

        message = u"""Booking {change} in to system.

{warning}
Link to booking: http://guild.house/bookings/{code}/

Link to day: http://guild.house/bookings/{url_day}

        Add event to calendar (only if big event)
        What: {pax}pax {name}
        When: {time} {date} {day}
        """.format(change=change,
                   warning=warning,
                   code=obj.code,
                   url=obj.get_absolute_url(),
                   method=form.cleaned_data.get('booking_method'),
                   day=form.cleaned_data.get('reserved_date').strftime('%a'),
                   time=str(form.cleaned_data.get('reserved_time')),
                   date=form.cleaned_data.get(
                       'reserved_date').strftime('%d-%b-%Y'),
                   url_day=form.cleaned_data.get(
                       'reserved_date').strftime('%Y/%m/%d/'),
                   pax=form.cleaned_data.get('party_size'),
                   name=form.cleaned_data.get('name'),
                   )
        subject = "[{method}] {name} {pax}pax {date} ".format(
            method=form.cleaned_data.get('booking_method'),
            date=form.cleaned_data.get('reserved_date').strftime('%a %d-%b'),
            pax=form.cleaned_data.get('party_size'),
            name=form.cleaned_data.get('name')
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.FROM_EMAIL,
            recipient_list=settings.TO_EMAILS,
        )
        return True

    def send_booking_notice_customer(self, obj, form):
        warning = ""
        if "full" in form.cleaned_data.get('private_notes'):
            warning = """
Beware! As warned at time of booking: you have booked during a busy time it is possible that your booking may have conflicted with another.

We will contact you ASAP if this is the case. Alternatively you can contact us to double-check.
        """

        message = u"""Thank you for making a reservation at Guild!

Name: {name}
Number of people: {pax}pax
When: {time}, {day} {date}
{warning}
Link to booking details: http://guild.house/bookings/{code}/success/

If you would like to contact us for any reason:
Call us on: 02 6257 2727
Email: hello@guild.house
Web: http://guild.house

--
Regards,
Automated Bookings Robot-Machine
-Guild Team

facebook.com/guildhouse.canberra
(02) 6257 2727
Open 7 days, 12pm til late
        """.format(code=obj.code,
                   warning=warning,
                   url=obj.get_absolute_url(),
                   method=form.cleaned_data.get('booking_method'),
                   day=form.cleaned_data.get('reserved_date').strftime('%a'),
                   time=str(form.cleaned_data.get('reserved_time')),
                   date=form.cleaned_data.get(
                       'reserved_date').strftime('%d-%b-%Y'),
                   pax=form.cleaned_data.get('party_size'),
                   name=form.cleaned_data.get('name'),
                   )
        subject = "[{method}] {name} {pax}pax {date} ".format(
            method=form.cleaned_data.get('booking_method'),
            date=form.cleaned_data.get('reserved_date').strftime('%a %d-%b'),
            pax=form.cleaned_data.get('party_size'),
            name=form.cleaned_data.get('name')
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.FROM_EMAIL,
            recipient_list=[form.cleaned_data.get('email')],
        )
        return True


class BookingQueryset(object):

    model = Booking
    allow_future = True
    date_field = 'reserved_date'
    month_format = '%m'
    week_format = "%W"
    paginate_by = settings.BOOKINGS_PAGINATE_BY

    def get_context_data(self, *args, **kwargs):
        context = super(BookingQueryset, self).get_context_data(
            *args, **kwargs)
        context['future_list'] = self.get_queryset().future()
        context['summary_list'] = self.get_queryset().today()\
                                      .values('reserved_date')\
                                      .annotate(count=Count('id'),
                                                pax=Sum('party_size'))\
                                      .order_by('reserved_date')
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super(BookingQueryset, self).get_queryset(*args, **kwargs)
        return queryset.active().order_by('reserved_date', 'reserved_time')

    def get_queryset_by_day(self, *args, **kwargs):
        queryset = super(BookingQueryset, self).get_queryset(*args, **kwargs)
        return queryset.active().order_by('reserved_date', 'reserved_time')


class BookingTimeView(BookingQueryset, TimeMixin, generic.ListView):

    template_name = 'bookings/_time.html'

    def get_context_data(self, *args, **kwargs):
        context = super(BookingTimeView, self).get_context_data(
            *args, **kwargs)
        context = self.get_time_list(context,
                                     this_date=date(int(self.kwargs['year']),
                                                    int(self.kwargs['month']),
                                                    int(self.kwargs['day']))
                                     )
        return context


class BookingSuccessView(BookingQueryset, generic.DetailView):

    template_name = 'bookings/booking_success.html'

    def get_object(self):
        return get_object_or_404(Booking, code=self.kwargs.get('code'))


class BookingRunView(LoginRequiredMixin, BookingQueryset, generic.DetailView):

    template_name = 'bookings/run_sheet.html'

    def get_object(self):
        return get_object_or_404(Booking, code=self.kwargs.get('code'))

    def get_context_data(self, *args, **kwargs):
        context = super(BookingRunView, self).get_context_data(
            *args, **kwargs)
        context['other_bookings'] = Booking.objects.filter(
            reserved_date=self.get_object().reserved_date)
        return context


class BookingCreateView(BookingFormMixin, CalendarMixin, BookingQueryset,
                        TimeMixin, generic.edit.CreateView):

    form_class = NewBookingForm

    def form_valid(self, form):
        obj = form.instance
        obj.save()
        self.send_booking_notice_internal(obj=obj, form=form, change="added")
        #self.send_booking_notice_customer(obj=obj, form=form)
        return redirect('bookings:booking_success', code=form.instance.code)

    def get_context_data(self, *args, **kwargs):
        context = super(BookingCreateView, self).get_context_data(
            *args, **kwargs)

        try:
            this_booking_date = BookingDate.objects.get(date=datetime.date.today())
            reservation_sheet_printed = this_booking_date.reservation_sheet_printed
        except BookingDate.DoesNotExist:
            reservation_sheet_printed = False

        start_date = datetime.date.today() if not reservation_sheet_printed else datetime.date.today() + datetime.timedelta(days=1)
        context = self.get_calendar(context, yr=start_date.year, mth=start_date.month, day=start_date.day)
        context['today'] = start_date
        context = self.get_time_list(context, this_date=start_date)
        return context

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(BookingCreateView, self).get_form_kwargs(
            *args, **kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        initial = super(BookingCreateView, self).get_initial()
        initial = initial.copy()

        if self.request.user.is_authenticated():
            initial['user'] = self.request.user
            initial['email'] = 'foh.managers@guild.house'

        # Set as tomorrow if booking made later than 6pm.
        if localtime(now()).hour > 18:
            initial['reserved_date'] = date.today() + timedelta(days=1)
        else:
            initial['reserved_date'] = date.today()
        initial['reserved_time'] = settings.DEFAULT_BOOKING_TIME
        initial['booking_duration'] = settings.DEFAULT_BOOKING_DURATION
        initial['booking_method'] = settings.DEFAULT_BOOKING_METHOD

        return initial


class BookingUpdateView(LoginRequiredMixin, BookingFormMixin, CalendarMixin,
                        BookingQueryset, generic.edit.UpdateView):

    slug_field = 'code'
    form_class = BookingForm

    def form_valid(self, form):
        obj = form.instance
        obj.updated_by = self.request.user
        obj.save()
        self.send_booking_notice_internal(obj=obj, form=form, change="updated")
        self.send_booking_notice_customer(obj=obj, form=form)
        return redirect('bookings:booking_update', code=form.instance.code)

    def get_object(self):
        if not self.request.user.is_authenticated():
            raise Http404()
        else:
            return get_object_or_404(Booking, code=self.kwargs.get('code'))

    def get_context_data(self, *args, **kwargs):
        context_data = super(BookingUpdateView, self).get_context_data(*args,
                                                                       **kwargs)
        obj = self.get_object()
        unique = self.get_queryset().filter(reserved_date=obj.reserved_date,
                                            phone=obj.phone)
        context_data['update_view'] = True
        return context_data


class BookingListView(BookingQueryset, generic.ListView):

    def get(self, *args, **kwargs):
        page = self.kwargs.get('page', None)
        if page is not None and int(page) < 2:
            return redirect('bookings:booking_list', permanent=True)
        return super(BookingListView, self).get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context_data = super(BookingListView, self).get_context_data(*args,
                                                                     **kwargs)
        context_data['show_all'] = True
        context_data['future_days_list'] = BookingDate.objects.future()
        return context_data


class BookingListNumView(LoginRequiredMixin, BookingListView):

    template_name = 'bookings/bookings_nums.html'


class BookingFutureView(LoginRequiredMixin, generic.ListView):

    model = BookingDate
    template_name = 'bookings/bookings_table.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super(BookingFutureView, self).get_queryset(*args, **kwargs)
        return queryset.future()

    def get_context_data(self, *args, **kwargs):
        get_future_services_set()
        context_data = super(
            BookingFutureView, self).get_context_data(*args, **kwargs)
        context_data['future_days_list'] = context_data['object_list']
        return context_data


class BookingCancelledView(BookingQueryset, generic.ListView):

    template_name = 'bookings/booking_list_cancelled.html'

    def get_queryset(self, *args, **kwargs):
        # queryset = super(BookingCancelledView, self).get_queryset(*args, **kwargs)
        return Booking.objects.filter(status__in=['cancelled', 'no_show']).order_by('-updated_at')


class BookingYearArchiveView(BookingQueryset, generic.YearArchiveView):

    make_object_list = True


class BookingMonthArchiveView(BookingQueryset, generic.MonthArchiveView):

    pass


class BookingDayArchiveView(BookingQueryset, generic.DayArchiveView):

    def get_context_data(self, *args, **kwargs):
        context_data = super(BookingDayArchiveView, self).get_context_data(*args,
                                                                           **kwargs)
        context_data['total'] = kwargs.get('object_list')\
                                      .aggregate(Sum('party_size'))
        services = []
        early_list = kwargs.get('object_list').filter(
            service='early').aggregate(Sum('party_size'))
        if early_list['party_size__sum']:
            services.append((('early', 'Early'), early_list))
        for serv in settings.SERVICE_CHOICE:
            services.append((serv, (kwargs.get('object_list').filter(service=serv[0])
                                    .aggregate(Sum('party_size')))))
        context_data['services'] = services
        context_data['cancelled_list'] = self.get_dated_queryset()\
                                             .filter(status='Cancelled')\
                                             .order_by('name')
        return context_data


class BookingTodayArchiveView(generic.RedirectView):

    def get_redirect_url(self):
        return reverse('bookings:booking_day', kwargs={
            'year': datetime.date.today().year,
            'month': "{:0>2}".format(datetime.date.today().month),
            'day': "{:0>2}".format(datetime.date.today().day)
        })


class BookingWeekArchiveView(BookingQueryset, generic.WeekArchiveView):

    pass


class BookingDetailView(BookingQueryset, generic.DetailView):

    pass


class FormView(generic.FormView):

    template_name = 'bookings/default_form.html'
    form_class = BlankForm
    success_url = "/bookings/post/"

class ReservationSheetView(BookingQueryset, generic.ListView):
    template_name = 'bookings/reservation_sheet.html'

    def get_queryset(self, *args, **kwargs):
        qs = super(ReservationSheetView, self).get_queryset(*args, **kwargs)
        return qs.filter(reserved_date=date.today())

    def get_context_data(self, *args, **kwargs):
        context_data = super(ReservationSheetView, self).get_context_data()
        table_layout = dict()
        table_layout["Inside"] = [str(i) for i in range(1,14)] + [str(i) for i in range(81,88)]
        table_layout["Outside"] = [str(i) for i in range(1,5)]
        context_data['table_layout'] = table_layout
        return context_data

class ReservationSheetPDFView(ReservationSheetView, WeasyTemplateResponseMixin):
    pdf_stylesheets = ['static/reservation_sheet.css','static/vendor/bootstrap/bootstrap.min.css']

    def get(self, request, *args, **kwargs):
        this_booking_date, _ = BookingDate.objects.get_or_create(date=datetime.date.today())
        print(this_booking_date)
        this_booking_date.reservation_sheet_printed = True
        this_booking_date.save()
        return super(ReservationSheetPDFView,self).get(request,*args,**kwargs)

def post_view(request):

    template_name = 'bookings/default_form.html'
    context_data = {}

    if request.method == 'POST':
        form = BlankForm(request.POST)
        if form.is_valid():
            print(request.POST)
            context_data['success_obj'] = import_revel_bookings(
                request.POST['input_data'])

    else:
        form = BlankForm()

    context_data['form'] = form
    return render(request, template_name, context_data)
