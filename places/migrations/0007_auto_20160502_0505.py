# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0006_grid_zone'),
    ]

    operations = [
        migrations.AddField(
            model_name='grid',
            name='count_place',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='grid',
            name='keyword',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
    ]
