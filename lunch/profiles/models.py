import hashlib
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from lunch.cards.models import Card

User = settings.AUTH_USER_MODEL

class Profile(models.Model):

    user = models.OneToOneField(User)
    graduation_date = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, **kwargs):
    created = kwargs.get('created', False)
    user = kwargs.get('instance')
    if created and user:
        uuid = hashlib.md5(str(timezone.now().timestamp).encode('utf-8')).hexdigest()
        Card.objects.create(uuid=uuid, user=user, active=True)
        Profile.objects.create(user=user)

