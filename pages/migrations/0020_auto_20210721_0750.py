# Generated by Django 3.2.5 on 2021-07-21 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0019_auto_20200730_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepageheader',
            name='end',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='homepageheader',
            name='start',
            field=models.DateField(default=None, null=True),
        ),
    ]
