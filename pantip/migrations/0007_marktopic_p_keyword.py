# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-25 15:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pantip', '0006_topic_p_keyword'),
    ]

    operations = [
        migrations.AddField(
            model_name='marktopic',
            name='p_keyword',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pantip.TopicKeyword'),
        ),
    ]
