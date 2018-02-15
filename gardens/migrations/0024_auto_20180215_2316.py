# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-02-15 23:16
from __future__ import unicode_literals

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gardens', '0023_auto_20180215_2314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maintenancephoto',
            name='main',
        ),
        migrations.AddField(
            model_name='maintenancephoto',
            name='large',
            field=image_cropping.fields.ImageRatioField('image', '600x400', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='large'),
        ),
    ]
