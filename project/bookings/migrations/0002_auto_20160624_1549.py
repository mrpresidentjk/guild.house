# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='code',
            field=models.CharField(default='', max_length=8, blank=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_method',
            field=models.CharField(default='phone', max_length=50, choices=[('phone', 'Phone'), ('email', 'Email'), ('facebook', 'Facebook'), ('person', 'In Person'), ('other', 'Other')]),
        ),
        migrations.AlterUniqueTogether(
            name='booking',
            unique_together=set([]),
        ),
    ]
