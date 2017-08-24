from django import template

register = template.Library()

@register.filter
def pax_total(bookings_list):
    return sum(booking.party_size for booking in bookings_list)
