# Generated by Django 4.0.2 on 2022-02-13 12:29

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0004_remove_uploadmodel_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadmodel',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='uuid.uuid1', editable=False, populate_from='files', unique=True),
        ),
    ]
