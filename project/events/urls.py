from django.conf.urls import include, url, patterns


urlpatterns = patterns('project.events.views',
    # url('^$', 'home','' ),
    url(r"^regular/(?P<id>.*)/(?P<slug>.*)/$", "event_recur", name="event_recur"),
    url(r"^(?P<year>.*)/(?P<month>.*)/(?P<day>.*)/(?P<slug>.*)/", "event_detail", name="event_detail"),
    url(r"^(?P<year>.*)/(?P<month>.*)/(?P<day>.*)/$", "event_day", name="event_day"),


    ## url(r"^(?P<year>.*)/(?P<month>.*)/$", "event_month", name="event_month"),
    ## url(r"^(?P<year>.*)/$", "event_year", name="event_year"),
)
