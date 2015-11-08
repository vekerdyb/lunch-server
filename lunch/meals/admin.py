from django.contrib import admin
from lunch.meals.models import Meal


class MealAdmin(admin.ModelAdmin):
    list_display = ('meal_type', 'get_full_name', 'date', 'available')
    list_filter = ('meal_type', 'date',)
    search_fields = ('profile__full_name', )
    ordering = ('date', 'meal_type', 'profile__full_name')

    def get_full_name(self, obj):
        return obj.profile.full_name

    get_full_name.short_description = "Full Name"
    get_full_name.admin_order_field = 'profile__full_name'



admin.site.register(Meal, MealAdmin)
