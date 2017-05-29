# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookings', '0007_auto_20160909_0001'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='updated_by',
            field=models.ForeignKey(related_name='booking_updated_by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='phone',
            field=models.CharField(help_text="One phone number only. Put additional numbers in 'notes' if necessary. We may need to confirm details so be sure to provide a good number.", max_length=100),
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(default=b'Booked', max_length=50, choices=[(b'Booked', b'Booked'), (b'Confirmed', b'Confirmed'), (b'Numbers Confirmed', b'Numbers Confirmed'), (b'Big Booking', b'Big Booking'), (b'Cancelled', b'Cancelled')]),
        ),
    ]
