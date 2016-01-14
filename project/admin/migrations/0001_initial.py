# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.db import migrations


def create_initial_sites(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    Site.objects.update_or_create(pk=1, defaults={'domain': 'guild.house',
                                                  'name': 'Guild'})


def create_initial_robots_rules(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    Url = apps.get_model('robots', 'Url')
    Rule = apps.get_model('robots', 'Rule')
    root, created = Url.objects.get_or_create(pattern='/')
    admin, created = Url.objects.get_or_create(pattern='/admin/')
    rule, created = Rule.objects.get_or_create(robot='*')
    rule.sites.add(Site.objects.first())
    rule.allowed.add(root)
    rule.disallowed.add(admin)


class Migration(migrations.Migration):

    dependencies = [
        ('robots', '0001_initial'),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_sites),
        migrations.RunPython(create_initial_robots_rules),
    ]
