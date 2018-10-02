from django.forms import ModelMultipleChoiceField, TextInput
from .models import Tag


class ModelCommaSeparatedChoiceField(ModelMultipleChoiceField):
    widget = TextInput

    def clean(self, value):
        if value is not None and value is not '':
            value = [item.strip() for item in value.split(",")]
            for v in value:
                v, created = Tag.objects.get_or_create(name=v)

        return super(ModelCommaSeparatedChoiceField, self).clean(value)
