# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-16 21:26
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gardens', '0014_worktype_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='worktype',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='Body'),
        ),
    ]
