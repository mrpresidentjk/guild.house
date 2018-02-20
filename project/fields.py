# -*- coding: utf-8 -*-
import re
from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django.forms.fields import CharField
from django.utils.encoding import force_text


PHONE_DIGITS_RE = re.compile(r'^(\d{8,10})$')


class AUPhoneNumberField(CharField):
    """
    A form field that validates input as an Australian phone number.
    Valid numbers have ten digits.
    """
    default_error_messages = {
        'invalid': 'Enter a valid phone number.'
    }

    def clean(self, value):
        """
        Validate a phone number. Strips parentheses, whitespace and hyphens.
        """
        super(AUPhoneNumberField, self).clean(value)
        if value in EMPTY_VALUES:
            return ''
        value = re.sub('(\(|\)|\s+|-)', '', force_text(value))
        phone_match = PHONE_DIGITS_RE.search(value)

        if phone_match:
            phone = phone_match.group(1)
            if len(phone) == 8 \
               or (len(phone) == 10 and str(phone[0]) == "0") \
               or (len(phone) == 11 and int(phone[0])):
                return '{}'.format(phone)
        raise ValidationError(self.error_messages['invalid'])
