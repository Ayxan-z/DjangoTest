# Generated by Django 4.0.2 on 2022-02-12 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadmodel',
            name='upload_file',
        ),
        migrations.AddField(
            model_name='uploadmodel',
            name='files',
            field=models.FileField(default='', upload_to='files', verbose_name='Fayl'),
            preserve_default=False,
        ),
    ]
