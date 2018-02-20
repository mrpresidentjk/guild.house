# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import project.blog.models
import django.utils.timezone
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(default='', max_length=200, blank=True)),
                ('heading', models.CharField(default='', max_length=200, blank=True)),
                ('featured_content', models.TextField(default='', blank=True)),
                ('content', models.TextField(default='', blank=True)),
                ('summary', models.TextField(default='', blank=True)),
                ('meta_description', models.CharField(default='', max_length=200, blank=True)),
                ('is_enabled', models.BooleanField(db_index=True, default=True, verbose_name='enabled')),
                ('is_featured', models.BooleanField(db_index=True, default=False, verbose_name='featured')),
                ('slug', models.SlugField(unique_for_date='publish_at')),
                ('publish_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('site', models.ForeignKey(default=project.blog.models.get_current_site, related_name='blog_entries', on_delete=django.db.models.deletion.PROTECT, to='sites.Site')),
                ('tags', taggit.managers.TaggableManager(through='taggit.TaggedItem', verbose_name='Tags', blank=True, help_text='A comma-separated list of tags.', to='taggit.Tag')),
            ],
            options={
                'verbose_name_plural': 'entries',
                'ordering': ['-publish_at', 'title'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='entry',
            unique_together=set([('site', 'publish_at', 'slug')]),
        ),
    ]
