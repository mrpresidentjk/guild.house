# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0005_auto_20160626_2348'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='booking_duration',
            field=models.DurationField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_method',
            field=models.CharField(default=b'phone', help_text='Only logged in people can see booking method.', max_length=50, choices=[(b'phone', b'Phone'), (b'email', b'Email'), (b'website', b'Online'), (b'facebook', b'Facebook Messenger'), (b'person', b'In Person'), (b'other', b'Other')]),
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(default=b'Added', max_length=50, choices=[(b'Added', b'Added'), (b'Confirmed', b'Confirmed'), (b'Numbers Confirmed', b'Numbers Confirmed'), (b'Big Booking', b'Big Booking'), (b'Cancelled', b'Cancelled')]),
        ),
    ]
