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
            'approved_by': self.user,
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

    def test_simple_temporary_member_create_blank_year(self):

        self.test_input.pop('year')
        test_temporarymember = TemporaryMember.objects.get(**self.test_input)
        self.assertEqual(self.new_temporarymember, test_temporarymember)

    def test_simple_temporary_member_create_blank_dob(self):

        self.test_input.pop('dob')
        test_temporarymember = TemporaryMember.objects.get(**self.test_input)
        self.assertEqual(self.new_temporarymember, test_temporarymember)

    def test_simple_temporary_member_convert_to_member(self):

        new_member = self.new_temporarymember.convert_to_member(
            payment_method='paypal',
            amount_paid='15.00',
            payment_ref='asdf',
            member_type=self.new_temporarymember.member_type,
        )

        # @TODO duplicated could be done smarter
        test_member_input = {
            'ref_name': 'Test',
            'sort_name': 'Smith',
            'emails__email': self.test_email,
            'phones__phone': self.test_phone,
            'address': '1 Testing Avenue',
            'postcode': '2601',
            'state': 'ACT',
            'country': 'Australia',
            'suburb': 'Canberra',
            'dob': date(1990, 1, 1),
            'year': 1234,
        }

        test_member = Member.objects.get(**test_member_input)
        self.assertEqual(new_member, test_member)

        test_membership_input = {
            'member': new_member,
            'member_type': self.new_temporarymember.member_type,
            'valid_from': self.new_temporarymember.approved_at,
            'valid_until': self.new_temporarymember.approved_at
            + timedelta(days=365),
        }

        test_membership = Membership.objects.get(**test_membership_input)

        self.assertEqual(new_member.membership_set.all()[0], test_membership)


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

        self.test_input1 = {
            'number': 1,
        }

        self.test_input2 = {
            'ref_name': 'Test',
            'sort_name': 'Smith',
            'address': '1 Testing Avenue',
            'postcode': '2601',
            'state': 'ACT',
            'country': 'Australia',
            'suburb': 'Canberra',
        }

        self.test_input3 = {
            'year': 1234,
        }

        self.test_input4 = {
            'dob': date(1990, 1, 1),
        }

    def test_members1(self):

        self.member = Member(**self.test_input1)
        self.member.save()
        member = Member.objects.get(**self.test_input1)
        self.assertEqual(self.member, member)

    def test_members2(self):

        self.member, is_created = Member.objects.update_or_create(
            **self.test_input1, defaults=self.test_input2)
        self.member.save()
        member = Member.objects.get(**self.test_input2)
        self.assertEqual(self.member, member)

    def test_members3(self):

        self.member, is_created = Member.objects.update_or_create(
            **self.test_input1, defaults=self.test_input3)
        self.member.save()
        member = Member.objects.get(**self.test_input3)
        self.assertEqual(self.member, member)

    def test_members4(self):

        self.member, is_created = Member.objects.update_or_create(
            **self.test_input1, defaults=self.test_input4)
        self.member.save()
        member = Member.objects.get(**self.test_input4)
        self.assertEqual(self.member, member)
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
        self.member = Member(**self.test_member_input)
        self.member.save()

        self.member.emails.add(self.test_email)
        self.member.phones.add(self.test_phone)

        self.test_membership_active = Membership(
            member=self.member,
            member_type='standard',
            valid_from=timezone.now() - timedelta(days=364),
            valid_until=timezone.now().date() + timedelta(days=1)
        )
        self.test_membership_active.save()

        self.test_membership_inactive = Membership(
            member=self.member,
            member_type='standard',
            valid_from=timezone.now() - timedelta(days=365),
            valid_until=timezone.now().date() - timedelta(days=1)
        )
        self.test_membership_inactive.save()

    def test_membership_active(self):

        self.assertTrue(self.test_membership_active.is_current())

    def test_membership_inactive(self):

        self.assertFalse(self.test_membership_inactive.is_current())

    def test_membership_queryset(self):

        test_list = [
            self.test_membership_active,
            self.test_membership_inactive,
        ]

        queryset_list = [x for x in self.member.membership_set.all()]

        self.assertEqual(test_list, queryset_list)

    def test_membership_queryset_active(self):

        test_list = [
            self.test_membership_active,
        ]

        queryset_list = [x for x in self.member.membership_set.active()]

        self.assertEqual(test_list, queryset_list)

    def test_membership_queryset_inactive(self):

        test_list = [
            self.test_membership_inactive,
        ]

        queryset_list = [x for x in self.member.membership_set.inactive()]

        self.assertEqual(test_list, queryset_list)

    def test_member_active(self):

        self.assertTrue(self.member.is_active())

    def test_member_inactive(self):

        self.test_membership_active.delete()

        self.assertFalse(self.member.is_active())
