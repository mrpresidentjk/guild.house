# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import taggit.managers
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='boardgamegeek_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='expansion_for',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, null=True, related_query_name='expansion', to='library.Game', related_name='expansions'),
        ),
        migrations.AddField(
            model_name='game',
            name='maximum_players',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='maximum_playtime',
            field=models.PositiveIntegerField(blank=True, help_text='Duration in minutes', null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='minimum_players',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='minimum_playtime',
            field=models.PositiveIntegerField(blank=True, help_text='Duration in minutes', null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='publisher',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='game',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags', through='taggit.TaggedItem', to='taggit.Tag'),
        ),
    ]
