# Generated by Django 2.0.4 on 2018-05-15 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('M', 'Mężczyzna'), ('F', 'Kobieta')], max_length=1),
        ),
    ]