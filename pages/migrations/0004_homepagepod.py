# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-23 19:51
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_delete_fosteringsubmission'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePagePod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Published'), (3, 'Unpublished'), (2, 'Draft')], default=1)),
                ('title', models.CharField(max_length=150)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Body')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('position', models.PositiveIntegerField(default=0)),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.node')),
            ],
            options={
                'verbose_name': 'Home Page Pod',
                'verbose_name_plural': 'Home Page Pods',
                'ordering': ('position',),
            },
        ),
    ]
