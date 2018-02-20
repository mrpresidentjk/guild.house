from django import template
from django.template import Node

from events.models import ComingEvent
register = template.Library()


class ComingEventNode(Node):
    def render(self, context):
        context['coming_events'] = ComingEvent.objects.filter(active=True)
        return ''

def get_coming_event(parser, token):
    return ComingEventNode()

get_custom_text = register.tag(get_coming_event)



