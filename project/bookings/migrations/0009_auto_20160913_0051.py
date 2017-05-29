# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0008_auto_20160912_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='busy_night',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='booking',
            name='private_notes',
            field=models.TextField(default='', blank=True),
        ),
    ]
