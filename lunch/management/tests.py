from django.test import TestCase
from lunch.management.commands.load_profiles import Command


class LoadProfiles(TestCase):
    command = Command

    def test_should_request_list_of_users_from_lunch_site(self):
        pass