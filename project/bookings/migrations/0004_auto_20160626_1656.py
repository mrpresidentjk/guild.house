# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0003_auto_20160626_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='phone',
            field=models.CharField(default='', help_text="One phone number only. Put additional numbers in 'notes' if necessary.", max_length=100, blank=True),
        ),
    ]
