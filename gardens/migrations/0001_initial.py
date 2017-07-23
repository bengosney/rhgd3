# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-22 21:43
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import image_cropping.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Garden',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Published'), (3, 'Unpublished'), (2, 'Draft')], default=1)),
                ('title', models.CharField(max_length=150)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Body')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='title')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('position', models.PositiveIntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GardenPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/gardens')),
                ('thumbnail', image_cropping.fields.ImageRatioField('image', '375x300', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='thumbnail')),
                ('position', models.PositiveIntegerField(default=0)),
                ('garden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gardens.Garden')),
            ],
            options={
                'verbose_name': 'Photo',
                'ordering': ('position',),
                'verbose_name_plural': 'Photos',
            },
        ),
        migrations.CreateModel(
            name='GardenType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Published'), (3, 'Unpublished'), (2, 'Draft')], default=1)),
                ('title', models.CharField(max_length=150)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='garden',
            name='gardentype',
            field=models.ManyToManyField(blank=True, to='gardens.GardenType'),
        ),
    ]
