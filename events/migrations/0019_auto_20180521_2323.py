# Generated by Django 2.0.4 on 2018-05-21 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_auto_20180521_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='tags',
            field=models.ManyToManyField(blank=True, help_text='Tagi mogą ułatwić odnalezienie Twojego spotkania (maks. 5)', to='events.Tag'),
        ),
    ]