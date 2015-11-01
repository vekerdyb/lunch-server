from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Card(models.Model):
    uuid = models.TextField(unique=True)
    profile = models.ForeignKey('profiles.Profile')
    active = models.BooleanField(default=True)
