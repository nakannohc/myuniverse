# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0005_place_grid'),
    ]

    operations = [
        migrations.AddField(
            model_name='grid',
            name='zone',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
