# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('place_type', models.CharField(max_length=50)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('scanned', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='place',
            name='name',
            field=models.CharField(max_length=250),
        ),
    ]
