from django.conf import settings
from django.core.management import BaseCommand
import requests


class Command(BaseCommand):
    def transform_raw_meal_data(self, raw):
        #raw = '0_1_0_0_0_1_0_0_1_0_0_0_0_0_0_1_0_0_0_0_0_0_1_1_0_1_0_0_0_1_0_0_1_1_1_0_0_0_0_1_1_1_1_0_0_0_1_1_1_1_0_0_0_0_1_0_1_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_'
        numbers = [x == '1' for x in raw.strip('_').split('_')]
        run_length = len(numbers) // 3
        a = numbers[:run_length]
        b = numbers[run_length:2 * run_length]
        c = numbers[2 * run_length:]

    def handle(self, *args, **options):
        params = {
            'req': '1',

        }
        requests.post(settings.PROFILES_URL, )
