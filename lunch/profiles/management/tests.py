import json
from unittest import mock

from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from lunch.profiles.management.commands.load_profiles import Command
from lunch.profiles.models import Profile


class LoadProfilesTest(TestCase):
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
                "1": "Full name 1",
                "2": "09",
                "diak_id": "1",
                "nev": "Full name 1",
                "kod": "09"
            },
            {
                "0": "2",
                "1": "Full name 2",
                "2": "13",
                "diak_id": "2",
                "nev": "Full name 2",
                "kod": "13"
            },
            {
                "0": "3",
                "1": "Full name 3",
                "2": "10",
                "diak_id": "3",
                "nev": "Full name 3",
                "kod": "10"
            },
        ]
        self.mock_good_response_object = self.ResponseMock(self.good_data)
        Profile.objects.all().delete()

    @mock.patch('lunch.profiles.management.commands.load_profiles.timezone')
    @mock.patch('lunch.profiles.management.commands.load_profiles.requests')
    def test_should_request_list_of_users_from_lunch_site(self, mock_requests, mock_timezone):
        mock_requests.post.return_value = self.mock_good_response_object
        mock_timezone.now.return_value = timezone.datetime(2015, 11, 1, 0, 0)
        self.command.handle()
        request_params = {
            'req': '1',
            'kerdes1': '201511'
        }
        mock_requests.post.assert_called_once_with(settings.PROFILES_URL, request_params)

    @mock.patch('lunch.profiles.management.commands.load_profiles.timezone')
    @mock.patch('lunch.profiles.management.commands.load_profiles.requests')
    def test_should_create_new_profiles(self, mock_requests, mock_timezone):
        self.assertEqual(Profile.objects.count(), 0)
        mock_requests.post.return_value = self.mock_good_response_object
        mock_timezone.now.return_value = timezone.datetime(2015, 11, 1, 0, 0)
        self.command.handle()
        profiles = Profile.objects.all().order_by('remote_system_id')
        self.assertEqual(profiles[0].remote_system_id, 1)
        self.assertEqual(profiles[0].full_name, 'Full name 1')
        self.assertEqual(profiles[0].year_of_graduation, 2020)

    @mock.patch('lunch.profiles.management.commands.load_profiles.timezone')
    @mock.patch('lunch.profiles.management.commands.load_profiles.requests')
    def test_should_calculate_year_of_graduation_correctly(self, mock_requests, mock_timezone):
        self.assertEqual(Profile.objects.count(), 0)
        mock_requests.post.return_value = self.mock_good_response_object
        mock_timezone.now.return_value = timezone.datetime(2015, 11, 1, 0, 0)
        self.command.handle()
        profiles = Profile.objects.get(remote_system_id=1)
        self.assertEqual(profiles.year_of_graduation, 2020)
        profiles = Profile.objects.get(remote_system_id=2)
        self.assertEqual(profiles.year_of_graduation, 2016)
        profiles = Profile.objects.get(remote_system_id=3)
        self.assertEqual(profiles.year_of_graduation, 2019)

    @mock.patch('lunch.profiles.management.commands.load_profiles.timezone')
    @mock.patch('lunch.profiles.management.commands.load_profiles.requests')
    def test_should_calculate_year_of_graduation_correctly_for_second_semester(self, mock_requests, mock_timezone):
        self.assertEqual(Profile.objects.count(), 0)
        mock_requests.post.return_value = self.mock_good_response_object
        mock_timezone.now.return_value = timezone.datetime(2016, 1, 1, 0, 0)
        self.command.handle()
        profiles = Profile.objects.get(remote_system_id=1)
        self.assertEqual(profiles.year_of_graduation, 2020)
        profiles = Profile.objects.get(remote_system_id=2)
        self.assertEqual(profiles.year_of_graduation, 2016)
        profiles = Profile.objects.get(remote_system_id=3)
        self.assertEqual(profiles.year_of_graduation, 2019)

    @mock.patch('lunch.profiles.management.commands.load_profiles.timezone')
    @mock.patch('lunch.profiles.management.commands.load_profiles.requests')
    def test_should_not_duplicate_users(self, mock_requests, mock_timezone):
        self.assertEqual(Profile.objects.count(), 0)
        mock_requests.post.return_value = self.mock_good_response_object
        mock_timezone.now.return_value = timezone.datetime(2016, 1, 1, 0, 0)
        self.command.handle()
        self.command.handle()
        profiles = Profile.objects.filter(remote_system_id=1)
        self.assertEqual(profiles.count(), 1)


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
    only_meal_1_every_day = generate_meal_string([range(1, 31), [], []], 31)
    meal_1_1_meal_2_2_meal_3_3 = generate_meal_string([[1], [2], [3]], 30)

    def test_meal_string_generator(self):
        meal_string = generate_meal_string([[1], [2], [31]], number_of_days=31)
        expected_string = '1_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_1_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_1_'
        self.assertEqual(meal_string, expected_string)

    def setUp(self):
        self.good_data = json.dumps(
            [
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
            ])
