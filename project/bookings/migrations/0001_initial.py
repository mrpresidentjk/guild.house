# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
import project.bookings.models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('party_size', models.PositiveIntegerField()),
                ('status', models.CharField(default='Confirmed', max_length=50, choices=[('Confirmed', 'Confirmed'), ('Unconfirmed', 'Unconfirmed'), ('Numbers Unconfirmed', 'Numbers Unconfirmed'), ('Big Booking', 'Big Booking'), ('Cancelled', 'Cancelled')])),
                ('notes', models.TextField(default='', blank=True)),
                ('email', models.EmailField(default='', max_length=254, blank=True)),
                ('phone', models.CharField(default='', max_length=100, blank=True)),
                ('booking_method', models.CharField(default='email', max_length=50, choices=[('email', 'Email'), ('phone', 'Phone'), ('facebook', 'Facebook'), ('person', 'In Person'), ('other', 'Other')])),
                ('reserved_date', models.DateField(default=django.utils.timezone.now, db_index=True)),
                ('reserved_time', models.TimeField(default=django.utils.timezone.now, db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('site', models.ForeignKey(related_name='bookings_booking', on_delete=django.db.models.deletion.PROTECT, default=project.bookings.models.get_current_site, to='sites.Site')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-reserved_date', 'reserved_time', 'name'],
                'verbose_name_plural': 'bookings',
            },
        ),
        migrations.AlterUniqueTogether(
            name='booking',
            unique_together=set([('site', 'reserved_date', 'reserved_time', 'phone')]),
        ),
    ]
