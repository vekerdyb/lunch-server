import datetime
import json

from django.conf import settings
from django.core.management import BaseCommand
import requests
from django.utils import timezone
from lunch.helpers.helpers import DateHelper
from lunch.profiles.models import Profile


class Command(BaseCommand):
    def get_graduation_date_from_class_code(self, code):
        code = int(code)
        today = timezone.now().date()
        this_year = today.year
        current_month = today.month
        if current_month > 6:
            modifier = 1
        else:
            modifier = 0
        graduation_date = datetime.date(this_year + 13 - code + modifier, 7, 1)
        return graduation_date

    def handle(self, *args, **options):
        month_string = timezone.now().strftime(DateHelper.MONTH_FORMAT_STRING)
        params = {
            'req': '1',
            'kerdes1': month_string,
        }
        response = requests.post(settings.PROFILES_URL, params)
        #TODO: test
        if response.text[:2] == '1#':
            response_data = json.loads(response.text[2:])
        else:
            response_data = response.json()
        for person in response_data:
            graduation_date = self.get_graduation_date_from_class_code(person['kod'])
            defaults = {
                'remote_system_id': person['diak_id'],
                'full_name': person['nev'],
            }
            Profile.objects.update_or_create(graduation_date=graduation_date, defaults=defaults)
