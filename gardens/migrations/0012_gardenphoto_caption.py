# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-09 21:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gardens', '0011_auto_20170806_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='gardenphoto',
            name='caption',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
