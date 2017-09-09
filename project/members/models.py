# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import timedelta
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django_date_extensions.fields import ApproximateDateField

from project.utils import get_current_site
from . import querysets, settings


    # ApproximateDate(
    #     blank=True, null=True,
    #     help_text="We don't like having to ask for this but we children members are differently categorised. Only year, or month and year are required.")  # noqa

@python_2_unicode_compatible
class Member(models.Model):

    # If multiple users: consolidate
    # @@TODO: switch off blank/null=True, ensure users exist or are generated
    user = models.ForeignKey('auth.User', blank=True, null=True)

    number = models.PositiveIntegerField()

    name = models.CharField(max_length=200, blank=True, default='',
                            verbose_name='Full Name',
                            )

    sort_name = models.CharField(max_length=200, blank=True, default='',
                                 verbose_name='Surname')

    ref_name = models.CharField(max_length=200, blank=True, default='',
                                verbose_name='First Name',
                                )

    title = models.CharField(max_length=64, blank=True, default='')

    notes = models.TextField(blank=True, default='')

    private_notes = models.TextField(blank=True, default='')

    emails = models.ManyToManyField('rolodex.Email', blank=True, null=True)

    phones = models.ManyToManyField('rolodex.Phone', blank=True, null=True)

    address = models.TextField(blank=True, default='')

    postcode = models.CharField(max_length=16, blank=True, default='')

    suburb = models.CharField(max_length=64, blank=True, default='')

    state = models.CharField(max_length=64, blank=True, default='')

    country = models.CharField(max_length=16, blank=True, default='Australia')

    year = models.PositiveIntegerField(blank=True, null=True)

    dob = models.DateField(
        blank=True, null=True, verbose_name='Birth date',
        help_text="Kept private.")
    #dob = ApproximateDateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=True)

    updated_at = models.DateTimeField(auto_now=True, editable=False)

    # @@TODO run cron last day of the month to turn on and off
    is_current = models.BooleanField(db_index=True, default=True)

    legacy_source = models.CharField(max_length=64, blank=True, default='')

    site = models.ForeignKey('sites.Site', default=get_current_site,
                             related_name='members_member',
                             on_delete=models.PROTECT)

    objects = querysets.MemberQuerySet.as_manager()

    def __str__(self):
        return "#{num} {name}".format(num=self.number,
                                      name=self.name)

    def save(self, *args, **kwargs):

        if not self.number:
            try:
                self.number = Member.objects.order_by('-number')[0].number + 1
            except IndexError:
                self.number = 1

        if not self.user:
            user = User.objects.create_user(username=self.number)
            user.first_name = self.ref_name
            user.last_name = self.sort_name
            user.save()
            self.user = user

        super(Member, self).save(*args, **kwargs)

    def is_active(self):
        if self.membership_set.active():
            return True
        else:
            return False

    def send_welcome_email(self):
        subject, from_email, to = 'hello', 'from@example.com', 'to@example.com'
        text_content = 'This is an important message.'
        html_content = '<p>This is an <strong>important</strong> message.</p>'

        message = """Thank you for becoming a Guild member """
        subject = """Thank you for becoming a Guild member """
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.FROM_EMAIL,
            recipient_list=settings.TO_EMAILS,
        )

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return True


class Membership(models.Model):

    member = models.ForeignKey('members.Member')

    member_type = models.CharField(max_length=255,
                                   choices=settings.MEMBERS_TYPES)

    valid_from = models.DateField(null=True, blank=False)

    valid_until = models.DateField(
        null=True, blank=False,
        help_text="""As the first day of the month following expiry. Eg. Nov 2018 = '1-Dec-2018'""")  # noqa

    objects = querysets.MembershipQuerySet.as_manager()

    def __str__(self):
        if self.is_current:
            current = " (current)"
        else:
            current = " (expired)"
        return "[{member_type}] {date} -- #{num} {name}".format(
            member_type=self.member_type,
            date=self.valid_until,
            num=self.member.number,
            name=self.member.name
        ) + current

    def is_current(self):
        if self.valid_until >= timezone.now():
            return True
        else:
            return False


class MembershipTag(models.Model):

    membership = models.ForeignKey('members.Membership')

    given_at = models.DateTimeField(auto_now_add=True, editable=True)

    given_tag = models.BooleanField()

    given_card = models.BooleanField()


@python_2_unicode_compatible
class Payment(models.Model):

    member = models.ForeignKey(Member)

    payment_method = models.CharField(max_length=128,
                                      choices=settings.PAYMENT_METHODS,
                                      default=settings.PAYMENT_METHODS[0][0])

    payment_ref = models.CharField(max_length=1024, blank=True, default='')

    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True, editable=True)

    class Meta(object):
        ordering = ['member__name', 'created_at']

    def __str__(self):
        return "#{num} ${amount_paid} [{payment_method}] ({name})".format(
            payment_method=self.payment_method,
            amount_paid=self.amount_paid,
            num=self.member.number,
            name=self.member.name
        )


class TemporaryMember(models.Model):
    """ Anybody can complete the form, it doesn't mean it's right and must be
    approved.
    """

    created_at = models.DateTimeField(auto_now_add=True)

    # APPROVAL manually added
    is_checked = models.BooleanField(default=False)

    is_approved_paid = models.BooleanField(default=False)

    approved_payment_method = models.CharField(
        max_length=255, blank=True, default='',
        choices=settings.PAYMENT_METHODS,
    )

    approved_by = models.ForeignKey('auth.User', blank=True, null=True)

    approved_at = models.DateTimeField(blank=True, null=True)

    # Payment type set by user, checked by staff
    payment_method = models.CharField(
        blank=True, default='',
        max_length=255, choices=settings.PAYMENT_METHODS,)

    payment_source = models.CharField(
        blank=True, default='',
        max_length=255, choices=settings.PAYMENT_METHODS,)

    # MEMBER
    # Member created automatically after manual staff approval
    member = models.ForeignKey('members.Member', blank=True, null=True)

    member_type = models.CharField(max_length=255,
                                   blank=True, default='',
                                   # exclude "special" as an option
                                   choices=settings.MEMBERS_TYPES[1:])

    # DETAILS
    # Replicable details for actual members
    name = models.CharField(max_length=200, blank=True, default='',
                            verbose_name='Full Name',)

    sort_name = models.CharField(
        max_length=200, verbose_name='Surname', blank=True, default='')

    ref_name = models.CharField(
        max_length=200, verbose_name='First Name', blank=True, default='')

    notes = models.TextField(blank=True, default='')

    email = models.ForeignKey('rolodex.Email', blank=True, default='')

    phone = models.ForeignKey('rolodex.Phone', blank=True, default='')

    address = models.TextField(blank=True, default=''),

    suburb = models.CharField(max_length=64)

    postcode = models.CharField(max_length=16)

    state = models.CharField(max_length=64)

    country = models.CharField(max_length=32, default='Australia')

    year = models.PositiveIntegerField(blank=True, null=True)

    dob = models.DateField(
        blank=True, null=True, verbose_name='Birth date',
        help_text="Kept private, necessary as licenced venue.")

    legacy_source = models.CharField(max_length=64, blank=True, default='')

    # SURVEY
    # Only kept in temporary for interest
    survey_games = models.TextField(
        blank=True, null=True,
        verbose_name="What's your favourite game?",
        help_text="List as many as you like.")
    survey_food = models.TextField(
        blank=True, null=True,
        verbose_name="What food, drink or pizza would you like see on our menu?",  # noqa
        help_text="Say as much as you want.")
    survey_hear = models.TextField(
        blank=True, null=True,
        verbose_name="How did you hear about us?",
        help_text="Tell us a story.")
    survey_suggestions = models.TextField(
        blank=True, null=True,
        verbose_name="Any suggestions you would have for us?",
        help_text="We're still pretty new and learning as we go!")

    def __str__(self):
        return "{}: {} {} [{}]".format(
            self.member_type,
            self.ref_name,
            self.sort_name,
            self.approved_at)

    def create_kwargs_set(**kwargs):

        return temporary_member_kwargs

    def get_or_create_member(self):
        """ What makes a member unique? """

        return member

    def convert_to_member(self, payment_method, amount_paid, payment_ref,
                          member_type):

        if self.member:
            return self.member

        # @@TODO github#7 make this more efficient
        new_member = Member()
        new_member.name = self.name
        new_member.sort_name = self.sort_name
        new_member.ref_name = self.ref_name
        new_member.notes = self.notes
        new_member.address = self.address
        new_member.postcode = self.postcode
        new_member.suburb = self.suburb
        new_member.state = self.state
        new_member.country = self.country
        new_member.dob = self.dob
        new_member.year = self.year
        new_member.save()

        new_member.emails.add(self.email)
        new_member.phones.add(self.phone)

        self.is_approved_paid = True
        self.is_checked = True
        self.approved_at = timezone.now()
        self.approved_payment_method = payment_method
        self.member = new_member
        self.save()

        new_payment = Payment()
        new_payment.member = new_member
        new_payment.payment_method = payment_method
        new_payment.payment_ref = payment_ref
        new_payment.amount_paid = amount_paid
        new_payment.created_at = timezone.now()
        new_payment.save()

        new_membership = Membership()
        new_membership.member = new_member
        new_membership.member_type = member_type
        new_membership.valid_from = self.approved_at
        new_membership.valid_until = self.approved_at + timedelta(days=365)
        new_membership.save()

        return new_member

    def save(self, *args, **kwargs):

        if not self.name:
            self.name = "{} {}".format(self.ref_name, self.sort_name)

        if self.is_approved_paid:
            if not self.approved_by or not self.approved_payment_method:
                raise Exception(
                    "If approved, must have payment method and user.")
            else:
                # create/check Member object exists
                pass

        return super(TemporaryMember, self).save(*args, **kwargs)
