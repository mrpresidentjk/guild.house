# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-22 22:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('members', '0003_auto_20170919_1839'),
    ]

    operations = [
        migrations.AddField(
            model_name='membershiptag',
            name='given_by',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='membershiptag',
            name='given_by_name',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='membershiptag',
            name='given_card',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='membershiptag',
            name='given_tag',
            field=models.BooleanField(default=False),
        ),
    ]
