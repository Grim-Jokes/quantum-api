# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-08 04:50
from __future__ import unicode_literals

from django.db import migrations, models


def empty(*args):
    pass


def move_descriptions(apps, *args):
    Transaction = apps.get_model('transactions', 'Transaction')
    Description = apps.get_model('transactions', 'Description')

    for description in Transaction.objects.values_list('description', flat=True).distinct():
        Description.objects.get_or_create(name=description)


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_category_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RunPython(
            move_descriptions, empty
        )
    ]