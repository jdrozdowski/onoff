# Generated by Django 2.0.4 on 2018-05-04 20:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20180504_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='max_number_of_participants',
            field=models.PositiveSmallIntegerField(default=2, validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(15)]),
        ),
        migrations.AlterField(
            model_name='event',
            name='min_number_of_participants',
            field=models.PositiveSmallIntegerField(default=2, validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(15)]),
        ),
    ]
