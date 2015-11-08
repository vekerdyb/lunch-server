from django.utils import timezone
from lunch.cards.models import Card
from lunch.meals.models import Meal
from lunch.meals.serializers import MealSerializer
from rest_framework.generics import RetrieveAPIView


class TodayMealByUUID(RetrieveAPIView):
    URL_NAME = 'profile-today-meal'

    queryset = Meal.objects.filter(available=True, date=timezone.now())
    serializer_class = MealSerializer

    class Meta:
        model = Meal

    def get_object(self):
        uuid = self.kwargs.pop('uuid')
        card = Card.objects.get(uuid=uuid)
        meal = self.queryset.filter(profile=card.profile).first()
        return meal
