from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from events.models import Event


class Chat(models.Model):
    event = models.OneToOneField(Event, on_delete=models.SET_NULL, null=True, blank=True)
    participants = models.ManyToManyField(User, blank=True)
    last_activity = models.DateTimeField(default=timezone.now)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    content = models.TextField(max_length=800)
