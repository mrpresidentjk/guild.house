# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0010_auto_20160914_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='legacy_code',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_duration',
            field=models.DurationField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='reserved_time',
            field=models.TimeField(default=django.utils.timezone.now, db_index=True),
        ),
    ]
