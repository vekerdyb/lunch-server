import datetime
from unittest import mock, skip
from lunch.cards.models import Card
from lunch.meals.factories import MealFactory
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
        Meal.objects.all().delete()

    def test_should_return_the_meal_option_for_the_person_with_uuid_for_today(self):
        profile = ProfileFactory(remote_system_id=1, full_name='Test Person')
        card = profile.card_set.first()
        MealFactory(profile=profile, meal_type=Meal.MEAL_A)
        response = self.client.get(reverse(self.url_name, kwargs={'uuid': card.uuid}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meal_type'], 'A')
        self.assertEqual(response.data['available'], True)
        self.assertEqual(response.data['full_name'], 'Test Person')

    @mock.patch('lunch.meals.views.timezone')
    def test_should_return_todays_meal(self, mock_timezone):
        now = datetime.datetime(2015, 11, 9, 0, 0)
        mock_timezone.now.return_value = now
        profile = ProfileFactory(remote_system_id=1, full_name='Test Person')
        card = profile.card_set.first()
        MealFactory(profile=profile, meal_type=Meal.MEAL_A, date=now.date())
        MealFactory(profile=profile, meal_type=Meal.MEAL_B, date=(now.date() - datetime.timedelta(days=1)))
        response = self.client.get(reverse(self.url_name, kwargs={'uuid': card.uuid}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meal_type'], 'A')

    def test_should_return_404_if_no_meal_for_person(self):
        profile = ProfileFactory(remote_system_id=1, full_name='Test Person')
        other_profile = ProfileFactory(remote_system_id=2, full_name='Test Person 2')
        other_persons_card = other_profile.card_set.first()
        MealFactory(profile=profile, meal_type=Meal.MEAL_A)
        response = self.client.get(reverse(self.url_name, kwargs={'uuid': other_persons_card.uuid}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
