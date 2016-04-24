# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0003_auto_20160424_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='address',
            field=models.TextField(default='no address'),
            preserve_default=False,
        ),
    ]
