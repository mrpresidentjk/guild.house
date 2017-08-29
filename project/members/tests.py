# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth.models import User
from django.test import TestCase  # , Client

from project.rolodex.models import Email, Phone
from .models import TemporaryMember


class TestTransactionSave(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            'test_staff_user', 'test@example.com', '1234')
        self.user.is_staff = True
        self.user.save()

    def test_simple_temporary_member_create(self):
        test_input = {
            'first_name': 'Test',
            'surname': 'Smith',
            'email': 'user@example.com',
            'phone': '0401234678',
            'address': '1 Testing Avenue',
            'postcode': '2601',
            'state': 'ACT',
            'country': 'Australia',
            'suburb': 'Canberra',
            'dob': datetime.date(1990, 1, 1),
            'payment_method': 'paypal',
            'survey_food': 'asdf',
            'survey_games': 'asdf',
            'survey_hear': 'asdf',
            'survey_suggestions': 'asdf',
        }
        new_temporarymember = TemporaryMember(**test_input)

        test_kwargs = {
            'first_name': 'Test',
            'surname': 'Smith',
            'address': '1 Testing Avenue',
            'postcode': '2601',
            'state': 'ACT',
            'country': 'Australia',
            'suburb': 'Canberra',
            'email': Email.objects.get(email='user@example.com'),
            'phone': Phone.objects.get(phone='0401234678'),
            'dob': datetime.date(1990, 1, 1),
            'payment_method': 'paypal',
            'survey_food': 'asdf',
            'survey_games': 'asdf',
            'survey_hear': 'asdf',
            'survey_suggestions': 'asdf',
        }
        test_temporarymember = TemporaryMember.objects.get(**test_kwargs)
        self.assertEqual(new_temporarymember, test_temporarymember)
