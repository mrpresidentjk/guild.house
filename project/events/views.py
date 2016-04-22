import datetime
from django.shortcuts import render_to_response, redirect#, get_object_or_404, get_list_or_404
from django.template import RequestContext
from models import Event, EventDate


def home(request, context={}, template='home.html'):
    ## spotlight
    today = datetime.datetime.today()-datetime.timedelta(days=1)
    spotlight = Event.objects.filter(spotlight=True).order_by('?')
    if spotlight.filter(date__gte=today):
        context['spotlights'] = spotlight.filter(date__gte=today)
    else:
        context['spotlights'] = spotlight[:4]
    context['events'] = Event.objects.filter(spotlight=False, recurring=False, date__gte=today).order_by('date')[:4]
    context['year'] = today.year
    return render_to_response(template, context_instance=RequestContext(request, context))


def entertainment(request, context={}, template='events/entertainment.html'):
    today = datetime.datetime.today()

    spotlight = Event.objects.filter(spotlight=True).order_by('?')
    if spotlight.filter(date__gte=today):
        context['spotlights'] = spotlight.filter(date__gte=today)
    else:
        context['spotlights'] = spotlight[:4]

    events = Event.objects.filter(spotlight=False, recurring=False, date__gte=today).order_by('?')
    context['entertains'] = entertains = events.filter(poster__pk__gt=0)[:2]

    ## the following upsets me
    context['events'] = events.exclude(id__in=[o.id for o in entertains])[:2]


    context['year'] = today.year
    #month_events = EventDate.objects.filter(date__month=today.month, date__year=today.year).order_by('date')
    next_month = today + datetime.timedelta(days=45)
    month_events = EventDate.objects.filter(date__gte=today, date__lte=next_month).order_by('date')
    context['month_events'] = month_events
    context['month_text'] = today
    return render_to_response(template, context_instance=RequestContext(request, context))


def check_update_date(event):
    if event.eventdate_set.count()>1:
        today = datetime.datetime.today()-datetime.timedelta(days=1)
        check = event.eventdate_set.filter(date__gte=today).order_by('date')
        if check:
            check = check[0]
            if event.date < check.date:
                event.date = check.date
                event.save()


def event_recur(request, id, slug, context={}, template='events/event.html'):
    ## event = get_object_or_404(Event, slug=slug, recurring=True)
    context['event'] = event = Event.objects.get(pk=id)#, recurring=True)
    try:
        context['recur'] = EventDate.objects.get(event=event, date=event.date)
    except:
        pass
    context['current_path'] = request.get_full_path()
    check_update_date(event)
    return render_to_response(template, context_instance=RequestContext(request, context))


def event_day(request, year, month, day, context={}, template='events/events.html'):
    day = datetime.date(year=int(year), month=int(month), day=int(day))
    context['events'] = event = Event.objects.filter(eventdate__date=day)
    ##context['day'] = True
    return render_to_response(template, context_instance=RequestContext(request, context))


def event_detail(request, year, month, day, slug, context={}, template='events/event.html'):
    day = datetime.date(year=int(year), month=int(month), day=int(day))
    context['event_detail'] = True
    try:
        event = Event.objects.filter(eventdate__date=day, slug=slug)[0]
    except:
        return redirect('/404/')
    if event.recurring:
        return redirect('/events/regular/%s/%s/' % (event.pk, event.slug))
    context['event'] = event
    context['current_path'] = request.get_full_path()
    check_update_date(event)
    return render_to_response(template, context_instance=RequestContext(request, context))
