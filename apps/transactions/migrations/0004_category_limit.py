# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-02 01:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_auto_20171101_0007'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='limit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
    ]