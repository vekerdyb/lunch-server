from django.contrib import admin
from lunch.profiles.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_email', 'uuid', 'user')

    def get_full_name(self, obj):
        return "%s %s" % (obj.user.first_name, obj.user.last_name)
    get_full_name.short_description = "Full Name"

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = "Email"


admin.site.register(Profile, ProfileAdmin)