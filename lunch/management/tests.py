from unittest import mock
from django.conf import settings
from django.test import TestCase
from lunch.management.commands.load_profiles import Command


class LoadProfiles(TestCase):
    command = Command()

    @mock.patch('lunch.management.commands.load_profiles.requests')
    def test_should_request_list_of_users_from_lunch_site(self, mock_requests):
        mock_requests.post.return_value = {}
        self.command.handle()
        mock_requests.post.assert_called_once_with(settings.PROFILES_URL)