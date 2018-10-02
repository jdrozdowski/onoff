from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.templatetags.static import static
from django.utils import timezone


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Mężczyzna'),
        ('F', 'Kobieta')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    birthdate = models.DateField(default=timezone.now)
    gender = models.CharField(
        default='',
        choices=GENDER_CHOICES,
        max_length=1,
    )
    city = models.CharField(
        max_length=30,
        blank=True,
        validators=[
            RegexValidator(
                regex='^[a-zA-ZąćęłńóśźżĄĘŁŃÓŚŹŻ.\s]+$',
                message='Wpisz poprawną nazwę miasta'
            )
        ]
    )
    description = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to='user_photo', blank=True)

    def photo_or_default(self, default_path="/img/photo.jpg"):
        if self.photo:
            return self.photo.url
        return static(default_path)


class Violation(models.Model):
    TABOO_WORDS = 'wulgaryzmy'
    HARASSEMENT = 'nękanie'
    ABSENCE = 'nieobecność'
    OTHER = 'inny'
    VIOLETION_CHOICES = (
        (TABOO_WORDS, 'Wulgarny język'),
        (HARASSEMENT, 'Nękanie'),
        (ABSENCE, 'Nieuczestnictwo w spotkaniu'),
        (OTHER, 'Inny powód')
    )

    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sender')
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    created_at = models.DateTimeField(default=timezone.now)
    violation = models.CharField(default='', choices=VIOLETION_CHOICES, max_length=255)
    comment = models.TextField(max_length=800)
