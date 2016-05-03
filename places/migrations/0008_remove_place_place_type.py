# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0007_auto_20160502_0505'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='place_type',
        ),
    ]
