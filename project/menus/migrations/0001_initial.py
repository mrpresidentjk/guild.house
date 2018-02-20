# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MenuType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default='', max_length=200, blank=True)),
                ('summary', models.TextField(default='', blank=True)),
                ('order', models.IntegerField(default=0)),
                ('is_enabled', models.BooleanField(default=True, db_index=True, verbose_name='enabled')),
                ('publish_at', models.DateTimeField(default=django.utils.timezone.now, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('menu_image', models.ImageField(default='', max_length=1024, upload_to='menu_image', blank=True)),
                ('menu_file', models.FileField(default='', max_length=1024, upload_to='menu_file', blank=True)),
            ],
        ),
    ]
