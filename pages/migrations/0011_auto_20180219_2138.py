# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-02-19 21:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0010_auto_20180219_2128'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sociallink',
            name='node_ptr',
        ),
        migrations.AlterField(
            model_name='contactsubmission',
            name='consent',
            field=models.BooleanField(verbose_name='I am over 18 and I give consent for data I enter into this form to be use to respond to my enquiry.'),
        ),
        migrations.AlterField(
            model_name='node',
            name='nav_icon',
            field=models.CharField(blank=True, choices=[('twitter-square', 'Twitter'), ('facebook-square', 'Facebook'), ('instagram', 'Instagram'), ('linkedin-square', 'LinkedIn')], max_length=200, null=True, verbose_name='Navigation Icon'),
        ),
        migrations.DeleteModel(
            name='SocialLink',
        ),
    ]
