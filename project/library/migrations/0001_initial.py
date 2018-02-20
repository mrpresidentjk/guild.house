# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import project.library.models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('title', models.CharField(default='', max_length=200, blank=True)),
                ('heading', models.CharField(default='', max_length=200, blank=True)),
                ('featured_content', models.TextField(default='', blank=True)),
                ('content', models.TextField(default='', blank=True)),
                ('meta_description', models.CharField(default='', max_length=200, blank=True)),
                ('is_enabled', models.BooleanField(verbose_name='enabled', default=True, db_index=True)),
                ('is_featured', models.BooleanField(verbose_name='featured', default=False, db_index=True)),
                ('slug', models.SlugField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('site', models.ForeignKey(related_name='library_categories', on_delete=django.db.models.deletion.PROTECT, to='sites.Site', default=project.library.models.get_current_site)),
            ],
            options={
                'verbose_name_plural': 'categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('title', models.CharField(default='', max_length=200, blank=True)),
                ('heading', models.CharField(default='', max_length=200, blank=True)),
                ('featured_content', models.TextField(default='', blank=True)),
                ('content', models.TextField(default='', blank=True)),
                ('meta_description', models.CharField(default='', max_length=200, blank=True)),
                ('is_enabled', models.BooleanField(verbose_name='enabled', default=True, db_index=True)),
                ('is_featured', models.BooleanField(verbose_name='featured', default=False, db_index=True)),
                ('slug', models.SlugField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('categories', models.ManyToManyField(related_name='games', related_query_name='game', to='library.Category')),
                ('site', models.ForeignKey(related_name='library_games', on_delete=django.db.models.deletion.PROTECT, to='sites.Site', default=project.library.models.get_current_site)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='game',
            unique_together=set([('site', 'slug')]),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('site', 'slug')]),
        ),
    ]
