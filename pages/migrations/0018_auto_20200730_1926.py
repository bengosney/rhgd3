# Generated by Django 3.0.8 on 2020-07-30 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0017_auto_20200730_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='title_tag',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Title Tag'),
        ),
    ]
