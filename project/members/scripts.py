# -*- coding: utf-8 -*-
"""
Script to generate members from spreadsheet one off.


- Generate `User` (username is `number`, password is phone number (or email))
- Generate `rolodex.Email` and `rolodex.Phone` objects.

"""
from .models import Member, Membership
from project.utils import convert_tsv


# Synchronising scrape from Revel to bookings system.
# To be automated daily.

def create_member(kwargs):

    obj, is_created = Member.objects.update_or_create(
        number=kwargs.pop('number'),
        defaults=kwargs)
    obj.save()
    return obj


def create_membership(kwargs):

    member, is_created = Member.objects.get_or_create(
        number=kwargs.pop('number'))
    obj, is_created = Membership.objects.update_or_create(
        member=member,
        member_type=kwargs.pop('member_type'),
        valid_from=kwargs.pop('valid_from'),
        defaults=kwargs)
    obj.save()
    return obj


def import_members(text):

    data = convert_tsv(text)
    success = []
    for kwargs in data:
        obj = create_member(kwargs=kwargs)
        success.append(obj)
    return success


def import_memberships(text):

    data = convert_tsv(text)
    success = []
    for kwargs in data:
        obj = create_membership(kwargs=kwargs)
        success.append(obj)
    return success
