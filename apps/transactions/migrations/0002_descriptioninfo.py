# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-19 04:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DescriptionInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max', models.DecimalField(decimal_places=2, max_digits=8)),
                ('min', models.DecimalField(decimal_places=2, max_digits=8)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.Category')),
            ],
        ),
    ]
