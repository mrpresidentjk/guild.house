# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import project.site.models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Homepage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('heading', models.CharField(default='', blank=True, max_length=200)),
                ('featured_content', models.TextField(default='', blank=True)),
                ('content', models.TextField(default='', blank=True)),
                ('meta_description', models.CharField(default='', blank=True, max_length=200)),
                ('is_enabled', models.BooleanField(verbose_name='enabled', default=True, db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('site', models.OneToOneField(to='sites.Site', on_delete=django.db.models.deletion.PROTECT, default=project.site.models.get_current_site)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
    ]
