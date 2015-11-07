from django.contrib import admin
from lunch.profiles.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'get_email', 'user', 'graduation_date', 'year_of_graduation')

    def get_email(self, obj):
        if obj.user:
            return obj.user.email
        return '<unknown>'
    get_email.short_description = "Email"

admin.site.register(Profile, ProfileAdmin)