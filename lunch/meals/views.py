from django.utils import timezone
from lunch.cards.models import Card
from lunch.meals.models import Meal
from lunch.meals.serializers import MealSerializer
from rest_framework.generics import RetrieveAPIView, get_object_or_404


class TodayMealByUUID(RetrieveAPIView):
    URL_NAME = 'profile-today-meal'

    queryset = Meal.objects.filter(available=True)
    serializer_class = MealSerializer

    class Meta:
        model = Meal

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        uuid = self.kwargs.pop('uuid')
        card = Card.objects.get(uuid=uuid)
        obj = get_object_or_404(queryset, profile=card.profile, date=timezone.now())
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj
