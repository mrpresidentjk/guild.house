from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.template.loader import get_template
from django.template import Context

from models import Event

class EventsFeed(Feed):
    title = "Transit Bar // Events"
    link = "/entertainment/"
    description = "Events. Check it."

    def items(self):
        return Event.objects.order_by('-date')[:5]

    def item_title(self, item):
        return item.event_name

    def item_description(self, item):
        t = get_template('feed_events.html')
        description = t.render(Context({'event': item}))
        return description

    def item_link(self, item):
        return '/events/%s/%s/%s/%s/' % (item.date.year, item.date.month, item.date.day, item.slug)

    ## author_name = 'Got a problem with oglaf.com?'
    ## author_email = 'tell.mistress@oglaf.com'


## site = Site.objects.get(id=settings.SITE_ID)
## path = '/events/%s/%s/%s/%s/' % (item.date.year, item.date.month, item.date.day, item.slug)
## return '%s/%s' % (site, path)
