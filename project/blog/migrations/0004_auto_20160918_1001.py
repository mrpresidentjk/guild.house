# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_entry_featured_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'ordering': ['featured_order', '-publish_at', 'title'], 'verbose_name_plural': 'entries'},
        ),
        migrations.AlterField(
            model_name='entry',
            name='featured_image',
            field=models.ImageField(default='', help_text='Ensure bigger than 790x377 if going to be featured in carousel.', max_length=1024, upload_to='entry_featured', blank=True),
        ),
    ]
