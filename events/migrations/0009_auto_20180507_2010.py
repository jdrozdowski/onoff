# Generated by Django 2.0.4 on 2018-05-07 18:10

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20180505_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.CharField(choices=[('sport', 'Sport'), ('muzyka', 'Muzyka'), ('nauka', 'Nauka'), ('sztuka', 'Sztuka'), ('gry', 'Gry'), ('pozostałe', 'Pozostałe')], default='sport', error_messages={'invalid_category': 'Wybierz istniejącą kategorię'}, max_length=9),
        ),
        migrations.AlterField(
            model_name='event',
            name='city',
            field=models.CharField(error_messages={'blank': 'Wpisz miasto, w którym odbędzie się spotkanie'}, max_length=30, validators=[django.core.validators.RegexValidator(message='Wpisz poprawną nazwę miasta', regex='^[A-Za-z.\\s]+$')]),
        ),
        migrations.AlterField(
            model_name='event',
            name='city_area',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='event',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 7, 18, 10, 20, 859947, tzinfo=utc), error_messages={'blank': 'Ustal termin spotkania'}, help_text='Możesz wpisać np. nazwę dzielnicy, osiedla, ulicy'),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(error_messages={'blank': 'Wpisz opis spotkania'}, max_length=280),
        ),
        migrations.AlterField(
            model_name='event',
            name='max_number_of_participants',
            field=models.PositiveSmallIntegerField(default=2, error_messages={'invalid': 'W spotkaniu może brać udział od 2 do 15 uczestników'}, help_text='Wprowadź liczbę uczestników od 2 do 15', validators=[django.core.validators.MinValueValidator(2, message='W spotkaniu muszą uczestniczyć conajmniej 2 uczestnicy'), django.core.validators.MaxValueValidator(15, message='W spotkaniu może uczesniczyć maksymalnie 15 uczestników')]),
        ),
        migrations.AlterField(
            model_name='event',
            name='min_number_of_participants',
            field=models.PositiveSmallIntegerField(default=2, error_messages={'invalid': 'W spotkaniu może brać udział od 2 do 15 uczestników'}, help_text='Możesz podać minimalną liczbę uczestników, aby spotkanie mogło się odbyć', validators=[django.core.validators.MinValueValidator(2, message='W spotkaniu muszą uczestniczyć conajmniej 2 uczestnicy'), django.core.validators.MaxValueValidator(15, message='W spotkaniu może uczesniczyć maksymalnie 15 uczestników')]),
        ),
        migrations.AlterField(
            model_name='event',
            name='tags',
            field=models.ManyToManyField(blank=True, help_text='Tagi mogą ułatwić odnalezienie Twojego spotkania (maks. 5)', limit_choices_to=5, to='events.Tag'),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(error_messages={'blank': 'Wpisz tytuł'}, max_length=25),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=24, unique=True, validators=[django.core.validators.RegexValidator(message='Tag może składać się z liter oraz liczb', regex='^[A-Za-z0-9.\\s]+$')]),
        ),
    ]