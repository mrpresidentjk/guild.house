# -*- coding: utf-8 -*-
from django.shortcuts import redirect, get_object_or_404, render
from django.views import generic

from project.rolodex.models import Email, Phone
from . import settings
from .forms import TemporaryMemberForm
from .models import TemporaryMember


def member_create_view(request):

    template_name = "members/member_form.html"
    context = {}

    if request.method == 'POST':
        form = TemporaryMemberForm(request.POST)
        if form.is_valid():
            temporary_member_kwargs = {}

            # Filter only necessary fields
            for field in settings.temporary_member_fields:
                temporary_member_kwargs[field] = request.POST.get(
                    field, '')

            # Replace string 'email'/'phone' with rolodex Model objects
            temporary_member_kwargs['email'], \
                created = Email.objects.get_or_create(
                    email=request.POST['email'])
            temporary_member_kwargs['phone'], \
                created = Phone.objects.get_or_create(
                    phone=request.POST['phone'])

            # Fix date format @TODO do this better
            dob = request.POST['dob'].split("/")
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

    if request.method == 'POST':
        temp_list = []

    else:
        temp_list = TemporaryMember.objects.filter(is_approved_paid=False)

    context['obj_list'] = temp_list

    return render(request, template_name, context)
