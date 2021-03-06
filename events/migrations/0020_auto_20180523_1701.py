# Generated by Django 2.0.4 on 2018-05-23 15:01

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0019_auto_20180521_2323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='created_at',
        ),
        migrations.AddField(
            model_name='event',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, error_messages={'blank': 'Ustal termin spotkania.'}),
        ),
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.CharField(choices=[('sport', 'Sport'), ('muzyka', 'Muzyka'), ('nauka', 'Nauka'), ('sztuka', 'Sztuka'), ('gry', 'Gry'), ('pozostałe', 'Pozostałe')], default='sport', error_messages={'invalid_category': 'Wybrana kategoria nie istnieje.'}, max_length=9),
        ),
        migrations.AlterField(
            model_name='event',
            name='city',
            field=models.CharField(error_messages={'blank': 'Wpisz nazwę miasta, w którym odbędzie się spotkanie.'}, max_length=30, validators=[django.core.validators.RegexValidator(message='Wpisz poprawną nazwę miasta.', regex='^[a-zA-ZąćęłńóśźżĄĘŁŃÓŚŹŻ.\\s]+$')]),
        ),
        migrations.AlterField(
            model_name='event',
            name='city_area',
            field=models.CharField(blank=True, help_text='Możesz wpisać nazwę ulicy, dzielnicy, osiedla itp.', max_length=30),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='event',
            name='max_number_of_participants',
            field=models.PositiveSmallIntegerField(default=2, error_messages={'invalid': 'W spotkaniu może wziąć udział od 2 do 16 uczestników.'}, help_text='Wprowadź liczbę uczestników (od 2 do 16).', validators=[django.core.validators.MinValueValidator(2, message='W spotkaniu muszą uczestniczyć conajmniej 2 uczestnicy.'), django.core.validators.MaxValueValidator(16, message='W spotkaniu może uczesniczyć maksymalnie 16 uczestników.')]),
        ),
        migrations.AlterField(
            model_name='event',
            name='min_number_of_participants',
            field=models.PositiveSmallIntegerField(blank=True, error_messages={'invalid': 'W spotkaniu może wziąć udział od 2 do 16 uczestników.'}, help_text='Możesz określić minimalną liczbę uczestników, aby spotkanie mogło się odbyć.', validators=[django.core.validators.MinValueValidator(2, message='W spotkaniu muszą uczestniczyć conajmniej 2 uczestnicy.'), django.core.validators.MaxValueValidator(16, message='W spotkaniu może uczesniczyć maksymalnie 16 uczestników.')]),
        ),
        migrations.AlterField(
            model_name='event',
            name='tags',
            field=models.ManyToManyField(blank=True, help_text='Tagi mogą ułatwić odnalezienie Twojego spotkania.', to='events.Tag'),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=35),
        ),
    ]
