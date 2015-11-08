import json
from copy import deepcopy
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
        mock_timezone.now.return_value = timezone.datetime(2015, 11, 1, 0, 0)

        self.command.handle()

        updated_data = deepcopy(self.good_data)
        updated_data[0]['nev'] = 'Updated name'
        updated_data[0]['kod'] = '12'
        updated_response_object = self.ResponseMock(updated_data)
        mock_requests.post.return_value = updated_response_object

        self.command.handle()

        profiles = Profile.objects.filter(remote_system_id=1)
        self.assertEqual(profiles.count(), 1)
        self.assertEqual(profiles[0].remote_system_id, 1)
        self.assertEqual(profiles[0].full_name, 'Updated name')
        self.assertEqual(profiles[0].year_of_graduation, 2017)