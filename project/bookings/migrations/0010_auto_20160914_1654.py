# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0009_auto_20160913_0051'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='area',
            field=models.CharField(default=b'inside', max_length=50, choices=[(b'inside', b'Inside'), (b'outside', b'Outside')]),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_duration',
            field=models.DurationField(blank=True, null=True, choices=[(b'0:15:00', b'15 minutes'), (b'0:30:00', b'30 minutes'), (b'0:45:00', b'45 minutes'), (b'1:00:00', b'1 hour'), (b'1:15:00', b'1 hour and 15 minutes'), (b'1:30:00', b'1 and a half hours'), (b'1:45:00', b'1 hour and 45 minutes'), (b'2:00:00', b'2 hours'), (b'2:30:00', b'2 and a half hours'), (b'3:00:00', b'more than 2 and a half hours')]),
        ),
        migrations.AlterField(
            model_name='booking',
            name='reserved_time',
            field=models.TimeField(default=django.utils.timezone.now, db_index=True, choices=[(datetime.time(12, 0), b'12:00'), (datetime.time(12, 30), b'12:30'), (datetime.time(13, 0), b'13:00'), (datetime.time(13, 30), b'13:30'), (datetime.time(14, 0), b'14:00'), (datetime.time(14, 30), b'14:30'), (datetime.time(15, 0), b'15:00'), (datetime.time(15, 30), b'15:30'), (datetime.time(16, 0), b'16:00'), (datetime.time(16, 30), b'16:30'), (datetime.time(17, 0), b'17:00'), (datetime.time(17, 30), b'17:30'), (datetime.time(18, 0), b'18:00'), (datetime.time(18, 30), b'18:30'), (datetime.time(19, 0), b'19:00'), (datetime.time(19, 30), b'19:30'), (datetime.time(20, 0), b'20:00'), (datetime.time(20, 30), b'20:30'), (datetime.time(21, 0), b'21:00'), (datetime.time(21, 30), b'21:30'), (datetime.time(22, 0), b'22:00'), (datetime.time(22, 30), b'22:30'), (datetime.time(23, 0), b'23:00')]),
        ),
    ]
