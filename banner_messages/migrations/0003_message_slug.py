# Generated by Django 3.0.5 on 2020-04-12 16:28

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('banner_messages', '0002_auto_20200412_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='title'),
        ),
    ]
