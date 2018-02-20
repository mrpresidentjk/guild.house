from django import template
from django.template import Node

from navigation.models import Menu, MenuItem
register = template.Library()


class TinyMenu(Node):
    def render(self, context):
        context['menu_items'] = MenuItem.objects.all().order_by('order')
        return ''


def get_menu(parser, token):
    return TinyMenu()

get_custom_text = register.tag(get_menu)



