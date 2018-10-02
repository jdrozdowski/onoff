from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, ModelForm, RadioSelect, SelectDateWidget, Textarea, ValidationError

from PIL import Image

from .models import UserProfile, Violation


class RegistrationForm(UserCreationForm):
    username = CharField(min_length=6, max_length=25, label='Nazwa użytkownika')

    class Meta:
        model = User

        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]

        labels = {
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'email': 'Adres e-mail'
        }

        def save(self, commit=True):
            user = super(RegistrationForm, self).save(commit=False)
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']

            if commit:
                user.save()

            return user

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise ValidationError("To pole jest wymagane.")

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name:
            raise ValidationError("To pole jest wymagane.")

        return last_name


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile

        fields = [
            'birthdate',
            'gender',
            'city',
            'description',
            'photo'
        ]

        labels = {
            'birthdate': 'Data urodzenia',
            'gender': 'Płeć',
            'city': 'Miasto',
            'description': 'O mnie',
            'photo': 'Zdjęcie profilowe'
        }

        widgets = {
            'birthdate': SelectDateWidget(
                years=range(2018, 1905, -1)
            ),
            'gender': RadioSelect(),
            'description': Textarea(attrs={'class': 'materialize-textarea'})
        }

    def clean_photo(self):
        image = self.cleaned_data['photo']
        if image:
            img = Image.open(image)
            width, height = img.size
            if img.width > 400 or img.height > 400:
                raise ValidationError("Zdjęcie ma nieodpowiednie wymiary. Maksymalna wielkość zdjęcia wynosi 400x400 px.")
        return image


class EditUserForm(ModelForm):
    class Meta:
        model = User

        fields = [
            'email',
            'first_name',
            'last_name'
        ]


class EditProfileForm(UserProfileForm):
    class Meta:
        model = UserProfile

        fields = [
            'gender',
            'city',
            'description',
            'photo'
        ]

        labels = {
            'gender': 'Płeć',
            'city': 'Miasto',
            'description': 'O mnie',
            'photo': 'Zdjęcie profilowe',
        }

        widgets = {
            'gender': RadioSelect(),
            'description': Textarea(attrs={'class': 'materialize-textarea'})
        }


class ReportUserForm(ModelForm):
    class Meta:
        model = Violation

        fields = [
            'violation',
            'comment'
        ]

        labels = {
            'violation': 'Wybierz powód zgłoszenia',
            'comment': 'Komentarz'
        }

        widgets = {
            'violation': RadioSelect(),
            'comment': Textarea(attrs={'class': 'materialize-textarea'})
        }
