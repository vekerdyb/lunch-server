from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

# Create your models here.
class Profile(models.Model):

    user = models.OneToOneField(User)
    graduation_date = models.DateField()
    uuid = models.TextField(unique=True)