from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from lunch.cards.helpers import CardQR
from lunch.profiles.models import Profile


class QRBaseView(TemplateView):
    template_name = "qr.html"

    def get_profile(self):
        raise NotImplementedError

    def get(self, request, *args, **kwargs):
        self.kwargs = kwargs
        profile = self.get_profile()
        base64_data_uri = CardQR(profile).get_base64_qr_data_uri()
        response_data = {'qr_code': base64_data_uri, 'full_name': profile.full_name}
        return render(request, self.template_name, response_data)


class MeView(QRBaseView):
    def get_profile(self):
        return self.request.user.profile


class CardView(QRBaseView):
    URL_NAME = 'profile-card'

    def get_profile(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Profile, remote_system_id=int(pk))
