from django.conf import settings
from django.shortcuts import render_to_response, redirect#, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.template.loader import select_template

from models import FoodBevPromo


def food_promos(request, context={}, template='foodbev/promos.html'):
    context['objects'] = FoodBevPromo.objects.filter(active=True).order_by('?', 'order')
    return render_to_response(template, context_instance=RequestContext(request, context))
