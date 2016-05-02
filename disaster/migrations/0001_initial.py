# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Disaster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField()),
                ('disaster_type', models.IntegerField(choices=[(1, b'Flood'), (2, b'Drought'), (3, b'Pest'), (4, b'Fire'), (5, b'Storm'), (6, b'Frozen'), (7, b'Hail'), (0, b'Others')])),
                ('area', models.FloatField()),
            ],
        ),
    ]
