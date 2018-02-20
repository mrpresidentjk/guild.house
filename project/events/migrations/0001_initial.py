# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('photologue', '0010_auto_20160105_1307'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_enabled', models.BooleanField(default=True)),
                ('spotlight', models.BooleanField(default=False)),
                ('spotlight_order', models.IntegerField(default=0)),
                ('recurring', models.BooleanField(default=False)),
                ('recur_description', models.CharField(default=b'', help_text=b"eg, 'Every Thursday'", max_length=255, verbose_name=b'Date Description', blank=True)),
                ('event_name', models.CharField(max_length=255)),
                ('slug', models.SlugField(default=b'', max_length=255, blank=True)),
                ('date', models.DateField(help_text=b"Events without dates aren't displayed, except if recurring.", null=True, blank=True)),
                ('time', models.TimeField(help_text=b'24 HOUR TIME. Add a usual time for recurring events. This will be over-ridden if specific time added.', null=True, blank=True)),
                ('expires', models.DateField(help_text=b'Optional.', null=True, blank=True)),
                ('paypal', models.CharField(default=b'', max_length=65, blank=True)),
                ('door_cost', models.CharField(default=b'', max_length=255, verbose_name=b'cost', blank=True)),
                ('ticket_url', models.URLField(default=b'', help_text=b'External ticket URL (if applicable)', blank=True)),
                ('gig_details', models.TextField(help_text=b'Short text. LIMITED TO 175 words.', max_length=999, verbose_name=b'Snippet Text')),
                ('content', models.TextField(default=b'', help_text=b'More artist info / bio.', blank=True)),
                ('extra_URLs', models.TextField(default=b'', help_text=b'eg. artist Myspace / website, separate multiple urls  with commas.', blank=True)),
                ('twitter_account', models.CharField(default=b'', max_length=100, blank=True)),
                ('facebook_event', models.CharField(default=b'', max_length=255, blank=True)),
                ('event_image', models.ForeignKey(related_name='event_image', blank=True, to='photologue.Photo', null=True)),
                ('extra_images', models.ManyToManyField(to='photologue.Photo', blank=True)),
                ('main_image', models.ForeignKey(related_name='main_image', blank=True, to='photologue.Photo', null=True)),
                ('post_event_gallery', models.ForeignKey(blank=True, to='photologue.Gallery', null=True)),
                ('poster', models.ForeignKey(related_name='poster', blank=True, to='photologue.Photo', null=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'ordering': ['-date', '-recurring'],
            },
        ),
        migrations.CreateModel(
            name='EventDate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('time', models.TimeField(null=True, blank=True)),
                ('additional', models.CharField(default=b'', help_text=b'Make it special.', max_length=999, blank=True)),
                ('date_image', models.ForeignKey(related_name='date_image', blank=True, to='photologue.Photo', null=True)),
                ('event', models.ForeignKey(to='events.Event')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='EventGallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=0)),
                ('event', models.ForeignKey(to='events.Event')),
                ('photo', models.ForeignKey(to='photologue.Photo')),
            ],
        ),
        migrations.CreateModel(
            name='EventUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('phone', models.CharField(default=b'', max_length=255, blank=True)),
                ('number_tickets', models.IntegerField(null=True)),
                ('amount_paid', models.DecimalField(null=True, max_digits=10, decimal_places=2)),
                ('event', models.ForeignKey(to='events.Event')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['event'],
            },
        ),
        migrations.CreateModel(
            name='EventVideo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('video', models.CharField(help_text=b'YouTube video link.', max_length=255, verbose_name=b'Youtube video')),
                ('order', models.IntegerField(default=0)),
                ('event', models.ForeignKey(to='events.Event')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
