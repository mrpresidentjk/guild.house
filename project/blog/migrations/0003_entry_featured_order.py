# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_entry_featured_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='featured_order',
            field=models.IntegerField(default=0),
        ),
    ]
