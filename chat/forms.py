from django.forms import ModelForm, CharField, Textarea, ValidationError

from .models import Message
from accounts.models import User


class MessageForm(ModelForm):
    class Meta:
        model = Message

        fields = ['content']

        labels = {
            'content': 'Napisz wiadomość'
        }

        widgets = {
            'content': Textarea(
                attrs={'class': 'materialize-textarea'}
            )
        }


class MessageWithReceiverForm(MessageForm):
    receiver = CharField(max_length=30, label="Odbiorca", help_text="Wpisz nazwę użytkownika, do którego chcesz wysłać wiadomość.")

    class Meta:
        model = Message
        fields = ['content']

        labels = {
            'content': 'Napisz wiadomość'
        }

        widgets = {
            'content': Textarea(
                attrs={'class': 'materialize-textarea'}
            )
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_receiver(self):
        person = self.cleaned_data['receiver']
        if person == self.user.username:
            raise ValidationError("Nie możesz wysłać wiadomości sam do siebie.")

        receiver = User.objects.filter(username=person)
        if not receiver:
            raise ValidationError("Użytkownik '%s' nie istnieje." % person)

        return receiver
