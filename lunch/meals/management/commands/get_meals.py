import datetime
import json
import logging

import requests
from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone
from lunch.helpers.helpers import DateHelper
from lunch.helpers.messages import MEAL_FOR_MISSING_PROFILE_ERROR
from lunch.meals.models import Meal
from lunch.profiles.models import Profile

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def transform_raw_meal_data(self, raw):
        # raw = '0_1_0_0_0_1_0_0_1_0_0_0_0_0_0_1_0_0_0_0_0_0_1_1_0_1_0_0_0_1_0_0_1_1_1_0_0_0_0_1_1_1_1_0_0_0_1_1_1_1_0_0_0_0_1_0_1_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_'
        if raw is None:
            return None
        numbers = [x == '1' for x in raw.strip('_').split('_')]
        run_length = len(numbers) // 3
        meal_a = numbers[:run_length]
        meal_b = numbers[run_length:2 * run_length]
        vegetarian = numbers[2 * run_length:]
        return meal_a, meal_b, vegetarian

    def handle(self, *args, **options):
        now = timezone.now()
        month_string = now.strftime(DateHelper.MONTH_FORMAT_STRING)
        params = {
            'req': '2',
            'kerdes1': month_string,
        }
        response = requests.post(settings.PROFILES_URL, params)
        if response.text[:2] == '1#':
            response_data = json.loads(response.text[2:])
        else:
            response_data = response.json()
        new_meals = []
        for item in response_data:
            user_id = item['diak_id']
            try:
                profile = Profile.objects.get(remote_system_id=user_id)
            except Profile.DoesNotExist:
                logger.error(MEAL_FOR_MISSING_PROFILE_ERROR.format(user_id))
            meals = self.transform_raw_meal_data(item['havikaja'])
            if meals and profile:
                for meal_type_index, meal_type in enumerate(meals):
                    for day, meal in enumerate(meal_type, start=1):
                        if meal:
                            data = {
                                'profile': profile,
                                'date': datetime.date(now.year, now.month, day)
                            }
                            defaults = {
                                'meal_type': Meal.MEAL_CHOICES[meal_type_index][0],
                            }
                            Meal.objects.update_or_create(defaults=defaults, **data)
