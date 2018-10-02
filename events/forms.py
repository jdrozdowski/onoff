from django.conf import settings
from django.forms import CharField, DateField, DateInput, Form, ModelChoiceField, ModelForm, RadioSelect, SplitDateTimeField, SplitDateTimeWidget, Textarea, ValidationError
from django.utils import timezone

from events.fields import ModelCommaSeparatedChoiceField
from events.models import Event, Tag


class EventForm(ModelForm):
    date = SplitDateTimeField(
        label='Termin spotkania',
        widget=SplitDateTimeWidget(
            date_attrs={'type': 'text', 'class': 'datepicker', 'placeholder': 'np. 01-01-2018'},
            time_attrs={'type': 'text', 'class': 'timepicker', 'placeholder': 'np. 20:30'}
        ),
        input_date_formats=settings.DATE_INPUT_FORMATS
    )

    tags = ModelCommaSeparatedChoiceField(
        label='Tagi',
        queryset=Tag.objects.all(),
        to_field_name='name',
        required=False,
        help_text="Dodaj tagi, aby Twoje spotknie było łatwiejsze do odnalezienia. Każdy tag musi być oddzielony od kolejnego przecinkiem (np. piłka nożna, hala)."
    )

    class Meta:
        model = Event
        fields = [
            'title',
            'category',
            'city',
            'city_area',
            'min_number_of_participants',
            'max_number_of_participants',
            'description',
        ]
        labels = {
            'title': 'Tytuł spotkania',
            'category': 'Kategoria',
            'city': 'Miasto',
            'city_area': 'Obszar miasta',
            'min_number_of_participants': 'Minimalna liczba uczestników',
            'max_number_of_participants': 'Maksymalna liczba uczestników',
            'description': 'Opis spotkania',
        }
        widgets = {
            'category': RadioSelect(),
            'description': Textarea(
                attrs={'class': 'materialize-textarea'}
            )
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['title'].disabled = True
            self.fields['category'].disabled = True,
            self.fields['city'].disabled = True,
            self.fields['description'].disabled = True,
            self.fields['tags'].disabled = True,

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now() + timezone.timedelta(minutes=30):
            raise ValidationError('Nie możesz stworzyć spotkania, do rozpoczęcia którego zostało mniej niż 30 minut.')

        return date

    def clean(self):
        cleaned_data = super(EventForm, self).clean()

        if cleaned_data['min_number_of_participants'] and cleaned_data['min_number_of_participants'] > cleaned_data['max_number_of_participants']:
            raise ValidationError('Minimalna liczba uczestników musi być mniejsza od maksymalnej liczby uczestników spotkania.')

        return cleaned_data


class PromoteToOrganizerForm(ModelForm):
    class Meta:
        model = Event

        fields = [
            'organizer'
        ]

        widgets = {
            'organizer': RadioSelect()
        }

    def __init__(self, *args, **kwargs):
        super(PromoteToOrganizerForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['organizer'] = ModelChoiceField(queryset=instance.participants.exclude(pk=instance.organizer.pk), label="Uczestnicy", empty_label=None)


class SearchEventForm(Form):
    date = DateField(label='Wybierz dzień', required=False, widget=DateInput(attrs={'class': 'datepicker'}), input_formats=settings.DATE_INPUT_FORMATS)
    query = CharField(label='Wpisz, czego szukasz', required=False)
    city = CharField(label='Miasto', required=False)
