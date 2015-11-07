from django.db import models
from django.utils.translation import ugettext as _
from lunch.profiles.models import Profile


class Meal(models.Model):
    MEAL_A = 'A'
    MEAL_B = 'B'
    MEAL_VEG = 'V'
    MEAL_CHOICES = (
        (MEAL_A, _('A')),
        (MEAL_B, _('B')),
        (MEAL_VEG, _('Vegetarian')),
    )

    meal_type = models.TextField(choices=MEAL_CHOICES)
    profile = models.ForeignKey(Profile)
    date = models.DateField()
    available = models.BooleanField(default=True)
