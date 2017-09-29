# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import binascii
import dateparser
import os
import re
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.models import Site
from django.utils.text import slugify


def get_current_site():
    try:
        return Site.objects.get_current().pk
    except Site.DoesNotExist:
        pass


def convert_tsv(dump):
    """ Make a sensible k,v dict from imported tsv.

    No validation is done here, just simple conversion.

    Returns list of dictionaries.
    """
    try:
        rows = [items for items in dump.split("\r\n")]
        header_row = rows[0].split("\t")
        list_row_dicts = []
        for item in rows[1:]:
            row_dict = dict(list(zip(header_row, item.split("\t"))))
            list_row_dicts.append(row_dict)
        return list_row_dicts
    except:
        raise Exception("""Failed to convert dump to dict.

All that is required is a copy and paste from a spreadsheet.""")


def make_date(value):
    """ Open to serious integrity error because of USA v. ISO8601 date
    variation, eg: 5-2-2017 v. 2-5-2017 (May or Feb?).

    Firmly enforce non-ambiguous date by Month as word eg: 2-May-2017.
    """
    month_as_word = re.sub(r'[^a-zA-Z.]', '', value)
    if not month_as_word:
        raise Exception(
            "Ambiguous date provided. Please provide month as word. eg: GOOD: 2-May-2017 BAD: 2017-02-05")  # noqa
    return dateparser.parse(value)


def generate_unique_slug(text, queryset, slug_field='slug', iteration=0):

    slug = slugify(text)
    if not slug:
        slug = '-'

    if iteration > 0:
        slug = '{0}-{1}'.format(iteration, slug)
    slug = slug[:50]

    try:
        queryset.get(**{slug_field: slug})
    except ObjectDoesNotExist:
        return slug
    else:
        iteration += 1
        return generate_unique_slug(text, queryset=queryset,
                                    slug_field=slug_field, iteration=iteration)


def generate_unique_hex(length=7, check_hex=None,
                        hex_field=None, queryset=None):
    key = binascii.hexlify(os.urandom(length)).decode('UTF-8')
    if check_hex:
        if key != check_hex:
            return key
        else:
            generate_unique_hex(check_hex=key)
    if queryset:
        if not queryset.filter(**{hex_field: key}):
            return key
        else:
            generate_unique_hex(queryset=queryset)
    return key
