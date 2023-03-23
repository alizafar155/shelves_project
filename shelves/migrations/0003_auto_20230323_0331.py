# Generated by Django 2.2.28 on 2023-03-23 03:31

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shelves', '0002_remove_userprofile_age'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='location',
        ),
        migrations.AlterField(
            model_name='media',
            name='releaseDate',
            field=models.DateField(blank=True, validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date.today)]),
        ),
    ]
