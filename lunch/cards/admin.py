from django.contrib import admin
from lunch.cards.models import Card


class CardAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'uuid', 'active')
    ordering = ('profile__full_name',)
    list_editable = ('active',)

    def get_full_name(self, obj):
        return obj.profile.full_name

    get_full_name.short_description = "Full Name"
    get_full_name.admin_order_field = 'profile__full_name'


admin.site.register(Card, CardAdmin)
