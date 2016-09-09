# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0006_auto_20160903_2333'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='hear_choices',
            field=models.CharField(default='', choices=[(b'event', b'event'), (b'facebook', b'facebook'), (b'friends', b'friends'), (b'newspaper', b'newspaper'), (b'search', b'search'), (b'other', b'other')], max_length=56, blank=True, help_text='How did you hear about us?', verbose_name='Choices'),
        ),
        migrations.AddField(
            model_name='booking',
            name='hear_other',
            field=models.TextField(default='', help_text='Tell us a story about how you heard about us ...', verbose_name='Other', blank=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='postcode',
            field=models.CharField(default='', max_length=16, blank=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='phone',
            field=models.CharField(default='', help_text="One phone number only. Put additional numbers in 'notes' if necessary. We may need to confirm details so be sure to provide a good number.", max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='reserved_date',
            field=models.DateField(db_index=True),
        ),
    ]
