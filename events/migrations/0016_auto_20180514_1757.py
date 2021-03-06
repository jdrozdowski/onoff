# Generated by Django 2.0.4 on 2018-05-14 15:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0015_event_organizer'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organizer', to=settings.AUTH_USER_MODEL),
        ),
    ]
