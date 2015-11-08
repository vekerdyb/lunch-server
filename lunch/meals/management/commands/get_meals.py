import json

import requests
from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone
from lunch.helpers.helpers import DateHelper


class Command(BaseCommand):
    def transform_raw_meal_data(self, raw):
        # raw = '0_1_0_0_0_1_0_0_1_0_0_0_0_0_0_1_0_0_0_0_0_0_1_1_0_1_0_0_0_1_0_0_1_1_1_0_0_0_0_1_1_1_1_0_0_0_1_1_1_1_0_0_0_0_1_0_1_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_'
        numbers = [x == '1' for x in raw.strip('_').split('_')]
        run_length = len(numbers) // 3
        meal_a = numbers[:run_length]
        meal_b = numbers[run_length:2 * run_length]
        vegetarian = numbers[2 * run_length:]
        return meal_a, meal_b, vegetarian

    def handle(self, *args, **options):
        month_string = timezone.now().strftime(DateHelper.MONTH_FORMAT_STRING)
        params = {
            'req': '2',
            'kerdes1': month_string,
        }
        response = requests.post(settings.PROFILES_URL, params)
        if response.text[:2] == '1#':
            response_data = json.loads(response.text[2:])
        else:
            response_data = response.json()
        for meal in response_data:
            pass
