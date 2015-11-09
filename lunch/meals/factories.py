import factory
from django.utils import timezone
from lunch.meals.models import Meal


class MealFactory(factory.DjangoModelFactory):
    class Meta:
        model = Meal

    date = timezone.now()