from django.contrib import admin
from lunch.cards.helpers import CardQR
from lunch.cards.models import Card
from lunch.profiles.views import CardView
from rest_framework.reverse import reverse


class CardAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'uuid', 'active', 'get_card_link',)
    ordering = ('profile__full_name',)
    list_editable = ('active',)

    def get_full_name(self, obj):
        return obj.profile.full_name

    get_full_name.short_description = 'Full Name'
    get_full_name.admin_order_field = 'profile__full_name'

    def get_card_link(self, obj):
        remote_system_id = obj.profile.remote_system_id
        full_name = obj.profile.full_name
        url = reverse(CardView.URL_NAME, kwargs={'pk': remote_system_id})
        qr = CardQR(obj.profile, box_size=1, border=0).get_base64_qr_data_uri()
        return '<img src="{}">&nbsp;<a href="{}">{}\'s card</a>'.format(qr, url, full_name)

    get_card_link.short_description = 'Link to card'
    get_card_link.allow_tags = True


admin.site.register(Card, CardAdmin)
