# Generated by Django 3.0.8 on 2020-07-30 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0014_auto_20200730_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='meta_description',
            field=models.TextField(blank=True, default=''),
        ),
    ]
