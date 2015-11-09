from lunch.meals.models import Meal
from rest_framework import serializers


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ('meal_type', 'available', 'full_name',)

    full_name = serializers.CharField(source='profile.full_name')
