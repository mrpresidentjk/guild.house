# -*- coding: utf-8 -*-
from datetime import date, timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from django.test import TestCase  # , Client

from project.rolodex.models import Email, Phone
from .models import TemporaryMember, Member, Membership


class TestTemporaryMemberSave(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            'test_staff_user', 'test@example.com', '1234')
        self.user.is_staff = True
        self.user.save()

        self.test_email, is_created = Email.objects.get_or_create(
            email='user@example.com')
        self.test_phone, is_created = Phone.objects.get_or_create(
            phone='0401234678')

        self.test_input = {
            'member_type': 'standard',
            'approved_at': timezone.now(),
            'ref_name': 'Test',
            'sort_name': 'Smith',
            'email': self.test_email,
            'phone': self.test_phone,
            'address': '1 Testing Avenue',
            'postcode': '2601',
            'state': 'ACT',
            'country': 'Australia',
            'suburb': 'Canberra',
            'dob': date(1990, 1, 1),
            'year': 1234,
            'payment_method': 'paypal',
            'survey_food': 'asdf',
            'survey_games': 'asdf',
            'survey_hear': 'asdf',
            'survey_suggestions': 'asdf',
        }
        self.new_temporarymember = TemporaryMember(**self.test_input)
        self.new_temporarymember.save()

    def test_simple_temporary_member_create(self):

        test_temporarymember = TemporaryMember.objects.get(**self.test_input)
        self.assertEqual(self.new_temporarymember, test_temporarymember)

class TestMembership(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            'test_staff_user', 'test@example.com', '1234')
        self.user.is_staff = True
        self.user.save()

        self.test_email, is_created = Email.objects.get_or_create(
            email='user@example.com')
        self.test_phone, is_created = Phone.objects.get_or_create(
            phone='0401234678')

        self.test_member_input = {
            'ref_name': 'Test',
            'sort_name': 'Smith',
            'address': '1 Testing Avenue',
            'postcode': '2601',
            'state': 'ACT',
            'country': 'Australia',
            'suburb': 'Canberra',
            'dob': date(1990, 1, 1),
            'year': 1234,
        }
        self.new_member = Member(**self.test_member_input)
        self.new_member.save()

        self.new_member.emails.add(self.test_email)
        self.new_member.phones.add(self.test_phone)

    def test_membership_active(self):

        test_membership = Membership(
            member=self.new_member,
            member_type='',
            valid_until=timezone.now() + timedelta(days=1)
        )
        test_membership.save()

        self.assertTrue(test_membership.is_current())

    def test_membership_inactive(self):

        test_membership = Membership(
            member=self.new_member,
            member_type='',
            valid_until=timezone.now() - timedelta(days=1)
        )
        test_membership.save()

        self.assertFalse(test_membership.is_current())
