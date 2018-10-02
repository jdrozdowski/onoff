from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinLengthValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(
        max_length=24,
        unique=True
    )

    def __str__(self):
        return self.name


class Event(models.Model):
    SPORT = 'sport'
    MUSIC = 'muzyka'
    LEARNING = 'nauka'
    ART = 'sztuka'
    GAMES = 'gry'
    OTHERS = 'pozostałe'

    CATEGORY_CHOICES = (
        (SPORT, 'Sport'),
        (MUSIC, 'Muzyka'),
        (LEARNING, 'Nauka'),
        (ART, 'Sztuka'),
        (GAMES, 'Gry'),
        (OTHERS, 'Pozostałe')
    )

    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organizer', null=True)
    title = models.CharField(
        max_length=35,
        validators=[MinLengthValidator(3)]
    )

    category = models.CharField(
        choices=CATEGORY_CHOICES,
        default=SPORT,
        max_length=9,
        error_messages={
            'invalid_category': 'Wybrana kategoria nie istnieje.'
        }
    )

    city = models.CharField(
        max_length=30,
        validators=[
            MinLengthValidator(3),
            RegexValidator(regex='^[a-zA-ZąćęłńóśźżĄĘŁŃÓŚŹŻ.\s]+$', message='Wpisz poprawną nazwę miasta.')
        ],
        error_messages={
            'blank': 'Wpisz nazwę miasta, w którym odbędzie się spotkanie.'
        }
    )

    city_area = models.CharField(
        max_length=30,
        validators=[MinLengthValidator(3)],
        blank=True,
        help_text="Możesz wpisać nazwę ulicy, dzielnicy, osiedla itp."
    )

    date = models.DateTimeField(
        default=timezone.now,
        error_messages={
            'blank': 'Ustal termin spotkania.'
        }
    )

    min_number_of_participants = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(2, message="W spotkaniu muszą uczestniczyć conajmniej 2 uczestnicy."),
            MaxValueValidator(16, message="W spotkaniu może uczesniczyć maksymalnie 16 uczestników.")
        ],
        help_text="Możesz określić minimalną liczbę uczestników, aby spotkanie mogło się odbyć.",
        error_messages={
            'invalid': 'W spotkaniu może wziąć udział od 2 do 16 uczestników.'
        }
    )

    max_number_of_participants = models.PositiveSmallIntegerField(
        default=2,
        validators=[
            MinValueValidator(2, message="W spotkaniu muszą uczestniczyć conajmniej 2 uczestnicy."),
            MaxValueValidator(16, message="W spotkaniu może uczesniczyć maksymalnie 16 uczestników.")
        ],
        help_text="Wprowadź liczbę uczestników (od 2 do 16).",
        error_messages={
            'invalid': 'W spotkaniu może wziąć udział od 2 do 16 uczestników.'
        },
    )

    description = models.TextField(
        max_length=500,
        validators=[MinLengthValidator(3)]
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        help_text="Tagi mogą ułatwić odnalezienie Twojego spotkania."
    )

    participants = models.ManyToManyField(User)

    def __str__(self):
        return self.title

    @property
    def is_expired(self):
        return self.date < timezone.now()
