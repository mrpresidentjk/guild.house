# -*- coding: utf-8 -*-
from django.views import generic

from .forms import TemporaryMemberForm


class MemberCreateView(generic.edit.CreateView):

    template_name = "members/member_form.html"
    form_class = TemporaryMemberForm

