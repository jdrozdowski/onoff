# Generated by Django 2.0.4 on 2018-05-05 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20180505_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=24, unique=True),
        ),
    ]
