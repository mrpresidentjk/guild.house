# -*- coding: utf-8 -*-
from django.shortcuts import redirect, get_object_or_404, render
from django.views import generic

from project.rolodex.models import Email, Phone
from .forms import TemporaryMemberForm
from .models import TemporaryMember


def member_create_view(request):

    template_name = "members/member_form.html"
    context = {}

    if request.method == 'POST':
        form = TemporaryMemberForm(request.POST)
        if form.is_valid():
            new = TemporaryMember(**request.POST)
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
