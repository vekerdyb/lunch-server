import json
from unittest import mock

from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from lunch.meals.models import Meal
from lunch.meals.management.commands.get_meals import Command


def generate_meal_string(data, number_of_days):
    """
    Data format:
    A list of lists.
    Sublists contain integers for the day of the month, when the meal option is payed for.
    E.g:
    [[1, 2, 28], [3, 5], []] means:
    - meal option 1 on 1st, 2nd, and 28th,
    - meal option 2 on 3rd, 5th
    - no days for meal option 3

    """
    meal_string = []
    days = range(1, number_of_days + 1)
    for meal_option in data:
        for day in days:
            if len(meal_option) > 0 and meal_option[0] == day:
                meal_string.append('1')
                meal_option = meal_option[1:]
            else:
                meal_string.append('0')
    return '_'.join(meal_string) + '_'


class LoadMealsTest(TestCase):
    only_meal_1_every_day = generate_meal_string([range(1, 31), [], []], 30)
    meal_1_1_meal_2_2_meal_3_3 = generate_meal_string([[1], [2], [3]], 30)

    def test_meal_string_generator(self):
        meal_string = generate_meal_string([[1], [2], [31]], number_of_days=31)
        expected_string = '1_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_1_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_1_'
        self.assertEqual(meal_string, expected_string)

    command = Command()

    class ResponseMock(object):
        def __init__(self, data):
            self.data = data
            self.content = '1#' + json.dumps(data)
            self.text = self.content

        def json(self):
            return self.data

    def setUp(self):
        self.good_data = [
            {
                "0": "1",
                "diak_id": "1",
                "1": self.only_meal_1_every_day,
                "havikaja": self.only_meal_1_every_day,
            },
            {
                "0": "230",
                "diak_id": "230",
                "1": self.only_meal_1_every_day,
                "havikaja": self.meal_1_1_meal_2_2_meal_3_3,
            },
            {
                "0": "231",
                "diak_id": "231",
                "1": None,
                "havikaja": None,
            }
        ]
        self.mock_good_response_object = self.ResponseMock(self.good_data)
        Meal.objects.all().delete()

    @mock.patch('lunch.meals.management.commands.get_meals.timezone')
    @mock.patch('lunch.meals.management.commands.get_meals.requests')
    def test_should_request_meals_from_backend_lunch_site(self, mock_requests, mock_timezone):
        mock_requests.post.return_value = self.mock_good_response_object
        mock_timezone.now.return_value = timezone.datetime(2015, 11, 1, 0, 0)
        self.command.handle()
        request_params = {
            'req': '2',
            'kerdes1': '201511'
        }
        mock_requests.post.assert_called_once_with(settings.MEALS_URL, request_params)

    @mock.patch('lunch.meals.management.commands.get_meals.timezone')
    @mock.patch('lunch.meals.management.commands.get_meals.requests')
    def test_should_create_meal_options_as_to_match_response_from_lunch_site(self, mock_requests, mock_timezone):
        mock_requests.post.return_value = self.mock_good_response_object
        mock_timezone.now.return_value = timezone.datetime(2015, 11, 1, 0, 0)
        self.command.handle()
        meals_for_user_1 = Meal.objects.filter(profile__remote_system_id=1)
        self.assertEqual(meals_for_user_1.count(), 30)

    @mock.patch('lunch.meals.management.commands.get_meals.timezone')
    @mock.patch('lunch.meals.management.commands.get_meals.requests')
    def test_should_update_existing_meal_options(self, mock_requests, mock_timezone):
        pass

    @mock.patch('lunch.meals.management.commands.get_meals.timezone')
    @mock.patch('lunch.meals.management.commands.get_meals.requests')
    def test_should_log_non_existing_students_with_meals(self, mock_requests, mock_timezone):
        pass
