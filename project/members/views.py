# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import redirect, render
from django.views import generic

from project.rolodex.models import Email, Phone
from . import settings
from .forms import TemporaryMemberForm, BlankForm
from .models import TemporaryMember, Member, Membership
from .scripts import import_members, import_memberships


def member_create_view(request):

    template_name = "members/member_form.html"
    context = {}

    if request.method == 'POST':
        form = TemporaryMemberForm(request.POST)
        if form.is_valid():
            temporary_member_kwargs = {}

            # Filter only necessary fields
            for field in settings.TEMPORARYMEMBER_FIELDS:
                temporary_member_kwargs[field] = request.POST.get(
                    field, '')

            # Tidy date fields
            if temporary_member_kwargs['dob'] == '':
                temporary_member_kwargs.pop('dob')

            if temporary_member_kwargs['year'] == '':
                temporary_member_kwargs.pop('year')

            # Replace string 'email'/'phone' with rolodex Model objects
            temporary_member_kwargs['email'], \
                created = Email.objects.get_or_create(
                    email=request.POST['email'])
            temporary_member_kwargs['phone'], \
                created = Phone.objects.get_or_create(
                    phone=request.POST['phone'])

            # Fix date format @TODO do this better
            dob = request.POST['dob'].split("/")
            if temporary_member_kwargs.get('dob', False):
                temporary_member_kwargs['dob'] = "{}-{}-{}".format(
                    dob[2], dob[1], dob[0])

            new_temporary_member = TemporaryMember(**temporary_member_kwargs)
            new_temporary_member.save()
            return redirect('/members/success/')
    else:
        form = TemporaryMemberForm()

    context['form'] = form

    return render(request, template_name, context)


class TemporaryMemberSuccessView(generic.TemplateView):

    template_name = "members/temporarymember_success.html"


def member_approval_view(request):

    template_name = "members/member_approval.html"
    context = {}
    temp_list = TemporaryMember.objects.filter(is_approved_paid=False)
    temp_list_new = temp_list.filter(is_checked=False).order_by('-pk')
    temp_list_old = temp_list.filter(is_checked=True).order_by('-pk')

    if request.method == 'POST':
        if request.POST.get('approve'):
            temporary_member = TemporaryMember.objects.get(
                pk=request.POST['pk'])
            temporary_member.approved_by = request.user
            temporary_member.save()

            new_member = temporary_member.convert_to_member(
                payment_method=request.POST['payment_method'],
                amount_paid=request.POST['amount_paid'],
                payment_ref=request.POST['payment_ref'],
                member_type=request.POST['member_type'],
            )
            context['new_member'] = new_member

        if request.POST.get('defer'):
            temporary_member = TemporaryMember.objects.get(
                pk=request.POST['pk'])
            temporary_member.approved_by = request.user
            temporary_member.is_checked = True
            temporary_member.save()

    context['obj_list_new'] = temp_list_new
    context['obj_list_old'] = temp_list_old
    context['payment_methods'] = settings.PAYMENT_METHODS
    context['member_types'] = settings.MEMBERS_TYPES

    return render(request, template_name, context)


class MemberListView(generic.list.ListView):

    model = Membership
    template_name = 'members/member_list.html'

    def get_queryset(self, **kwargs):
        return Membership.objects.all()


def member_detail_view(request, number):

    template_name = 'members/member_detail.html'
    context = {}

    member = Member.objects.filter(number=number)

    if member:
        context['obj'] = member[0]
    else:
        raise Http404

    return render(request, template_name, context)


def import_view(request):

    template_name = 'members/default_form.html'
    context = {}

    if request.method == 'POST':
        form = BlankForm(request.POST)
        if form.is_valid():
            if request.POST['input_class'] == 'member':
                context['success_obj'] = import_members(
                    request.POST['input_data'])
            if request.POST['input_class'] == 'membership':
                context['success_obj'] = import_memberships(
                    request.POST['input_data'])
                context['class'] = 'membership'
    else:
        form = BlankForm()

    context['form'] = form
    return render(request, template_name, context)
