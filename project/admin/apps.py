# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django import apps


class AppConfig(apps.AppConfig):

    label = 'project_admin'

    name = 'project.admin'

    verbose_name = 'Administration'
