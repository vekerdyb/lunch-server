import hashlib

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from lunch.cards.models import Card

User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    user = models.OneToOneField(User, null=True)
    full_name = models.TextField()
    remote_system_id = models.IntegerField(unique=True)
    graduation_date = models.DateField(null=True, blank=True)
    year_of_graduation = models.IntegerField(null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.graduation_date:
            self.year_of_graduation = self.graduation_date.year
        super(Profile, self).save(force_insert, force_update, using, update_fields)


@receiver(post_save, sender=Profile)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created and instance:
        seed = str(timezone.now().timestamp).encode('utf-8')
        seed += str(instance.id).encode('utf-8')
        uuid = hashlib.md5(seed).hexdigest()
        Card.objects.create(uuid=uuid, profile=instance, active=True)
