# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0004_place_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='grid',
            field=models.ForeignKey(blank=True, to='places.Grid', null=True),
        ),
    ]
