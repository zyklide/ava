# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-07 02:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluatesender',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]