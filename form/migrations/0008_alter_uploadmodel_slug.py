# Generated by Django 4.0.2 on 2022-02-13 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0007_alter_uploadmodel_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadmodel',
            name='slug',
            field=models.SlugField(),
        ),
    ]