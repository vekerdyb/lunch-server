from lunch.cards.models import Card
from lunch.meals.models import Meal
from lunch.meals.views import TodayMealByUUID
from lunch.profiles.factories import ProfileFactory
from lunch.profiles.models import Profile
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class TodayMealByUUIDTest(APITestCase):
    url_name = TodayMealByUUID.URL_NAME

    def setUp(self):
        Card.objects.all().delete()
        Profile.objects.all().delete()

    def test_should_return_the_meal_option_for_the_person_with_uuid_for_today(self):
        profile = ProfileFactory(remote_system_id=1, full_name='Test Person')
        card = profile.card_set.first()
        Meal(profile=profile, meal_type=Meal.MEAL_A)
        response = self.client.get(reverse(self.url_name, kwargs={'uuid': card.uuid}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
