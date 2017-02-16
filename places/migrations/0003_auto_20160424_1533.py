# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0002_auto_20160419_0902'),
    ]

    operations = [
        migrations.AddField(
            model_name='grid',
            name='x',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grid',
            name='y',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
