import base64
import io
from django.shortcuts import render
from django.views.generic import TemplateView
import qrcode
from rest_framework.generics import RetrieveAPIView


class MeView(TemplateView):
    template_name = "me.html"

    def get_qr_image(self, request):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(request.user.profile.card_set.filter(active=True)[0].uuid)
        qr.make(fit=True)
        return qr.make_image()

    def get_base64_qr_data_uri(self, request):
        image_buffer = io.BytesIO()
        image = self.get_qr_image(request)
        image.save(image_buffer)
        base64_string = base64.b64encode(image_buffer.getvalue()).decode()
        return "data:image/png;base64,{0}".format(base64_string)

    def get(self, request, *args, **kwargs):
        base64_data_uri = self.get_base64_qr_data_uri(request)
        response_data = {'qr_code': base64_data_uri}
        return render(request, self.template_name, response_data)


class OptionByUUID(RetrieveAPIView):
    pass