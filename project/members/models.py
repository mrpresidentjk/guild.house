# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django_date_extensions.fields import ApproximateDateField

from project.utils import get_current_site
from . import querysets, settings


class TemporaryMember(models.Model):
    """ Anybody can complete the form, it doesn't mean it's right and must be
    approved.
    """

    created_at = models.DateTimeField(auto_now_add=True)

    is_checked = models.BooleanField(default=False)

    is_approved_paid = models.BooleanField(default=False)

    approved_payment_method = models.CharField(
        max_length=255, blank=True, default='',
        choices=settings.PAYMENT_METHODS,
    )

    approved_by = models.ForeignKey('auth.User', blank=True, null=True)

    name = models.CharField(max_length=200, blank=True, default='',
                            verbose_name='Full Name',
                            )

    sort_name = models.CharField(max_length=200, blank=True, default='',
                                 verbose_name='Surname')

    ref_name = models.CharField(max_length=200, blank=True, default='',
                                verbose_name='First Name',
                                )

    notes = models.TextField(blank=True, default='')

    email = models.ManyToManyField('rolodex.Email')

    phone = models.ManyToManyField('rolodex.Phone')

    address = models.TextField(blank=True, default='')

    postcode = models.CharField(max_length=16, blank=True, default='')

    state = models.CharField(max_length=16, blank=True, default='')

    country = models.CharField(max_length=16, blank=True, default='Australia')

    # ApproximateDateField(
    # blank=True, null=True,
    # help_text="We don't like having to ask for this but we children members are differently categorised. Only year, or month and year are required.")  # noqa
    dob = ApproximateDateField(
        blank=True, null=True,
        help_text="We don't like having to ask for this but we children members are differently categorised. Only year, or month and year are required.")  # noqa

    payment_method = models.CharField(
        max_length=255, choices=settings.PAYMENT_METHODS,)

    survey_suggestions = models.TextField(
        blank=True, null=True,
        help_text="Any suggestions you would have for us?")
    survey_hear = models.TextField(
        blank=True, null=True,
        help_text="How did you hear about us? Tell us a story.")
    survey_food = models.TextField(
        blank=True, null=True,
        help_text="What food, drink or pizza would you like see on our menu? Say as much as you want.")  # noqa
    survey_games = models.TextField(
        blank=True, null=True,
        help_text="What's your favourite game? List as many as you like.")

    def save(self, *args, **kwargs):

        if self.is_approved_paid:
            if not self.approved_by or not self.approved_payment_method:
                raise Exception(
                    "If approved, must have payment method and user.")

        return super(TemporaryMember, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Member(models.Model):

    # If multiple users: consolidate
    # @@TODO: switch off blank/null=True, ensure users exist or are generated
    user = models.ForeignKey('auth.User', blank=True, null=True)

    member_number = models.PositiveIntegerField()

    name = models.CharField(max_length=200, blank=True, default='',
                            verbose_name='Full Name',
                            )

    sort_name = models.CharField(max_length=200, blank=True, default='',
                                 verbose_name='Surname')

    ref_name = models.CharField(max_length=200, blank=True, default='',
                                verbose_name='First Name',
                                )

    notes = models.TextField(blank=True, default='')

    private_notes = models.TextField(blank=True, default='')

    email = models.ManyToManyField('rolodex.Email')

    phone = models.ManyToManyField('rolodex.Phone')

    address = models.TextField(blank=True, default='')

    postcode = models.CharField(max_length=16, blank=True, default='')

    state = models.CharField(max_length=16, blank=True, default='')

    country = models.CharField(max_length=16, blank=True, default='Australia')

    #dob = ApproximateDateField(blank=True, null=True)
    dob = ApproximateDateField(blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True, editable=False)

    # @@TODO run cron last day of the month to turn on and off
    is_current = models.BooleanField(db_index=True, default=True)

    site = models.ForeignKey('sites.Site', default=get_current_site,
                             related_name='members_member',
                             on_delete=models.PROTECT)

    def __str__(self):
        return "#{num} {name}".format(date=self.valid_until,
                                      num=self.number,
                                      name=self.name)

    def save(self, *args, **kwargs):

        if not self.user:
            user = User.objects.create_user(username=self.member_number)
            user.first_name = self.ref_name
            user.last_name = self.sort_name
            user.save()
            self.user = user

        super(Member, self).save(*args, **kwargs)

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

    member_type = models.CharField(max_length=255)

    valid_from = models.DateField(null=True, blank=False)

    valid_until = models.DateField(
        null=True, blank=False,
        help_text="""As the first day of the month following expiry. Eg. Nov 2018 = '1-Dec-2018'""")  # noqa


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
                                      default=settings.PAYMENT_METHODS[0][0]
                                      )

    payment_ref = models.CharField(max_length=1024, blank=True, default='')

    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True, editable=True)

    objects = querysets.QuerySet.as_manager()

    class Meta(object):
        ordering = ['member__name', 'created_at']

    def __str__(self):
        return "{date} #{num} {name}".format(
            date=self.valid_until,
            num=self.member.number,
            name=self.member.name
        )
