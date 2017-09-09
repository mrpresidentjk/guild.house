# -*- coding: utf-8 -*-
"""
Script to generate members from spreadsheet one off.


- Generate `User` (username is `number`, password is phone number (or email))
- Generate `rolodex.Email` and `rolodex.Phone` objects.

"""
from .models import Member
from project.utils import convert_tsv


# Synchronising scrape from Revel to bookings system.
# To be automated daily.


def import_members(scrape):

    data = convert_tsv(scrape)

    success = []
    for kwargs in data:
        obj = Member(number=kwargs.pop('number'), **kwargs)
        obj.save()
        print(obj)
        success.append(obj)
    return success
