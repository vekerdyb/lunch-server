from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Card(models.Model):
    uuid = models.TextField(unique=True)
    user = models.ForeignKey(User)
    active = models.BooleanField(default=True)
