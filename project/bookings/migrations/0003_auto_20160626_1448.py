# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_auto_20160624_1549'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='booking',
            options={'ordering': ['reserved_date', 'reserved_time', 'name'], 'verbose_name_plural': 'bookings'},
        ),
        migrations.AddField(
            model_name='booking',
            name='service',
            field=models.CharField(default='', max_length=50, blank=True, choices=[('lunch', 'Lunch'), ('afternoon', 'Afternoon'), ('main', 'Main')]),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_method',
            field=models.CharField(default='phone', max_length=50, choices=[('phone', 'Phone'), ('email', 'Email'), ('website', 'Online'), ('facebook', 'Facebook Messenger'), ('person', 'In Person'), ('other', 'Other')]),
        ),
    ]
