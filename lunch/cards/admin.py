from django.contrib import admin

# Register your models here.
from lunch.cards.models import Card

class CardAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'uuid', 'active')

    def get_full_name(self, obj):
        return "%s %s" % (obj.user.first_name, obj.user.last_name)
    get_full_name.short_description = "Full Name"

admin.site.register(Card, CardAdmin)