import base64
import io

import qrcode


class CardQR(object):
    def __init__(self, profile, box_size=10, border=4):
        self.profile = profile
        self.box_size = box_size
        self.border = border

    def _get_active_card_uuid(self):
        return self.profile.card_set.filter(active=True)[0].uuid

    def _get_qr_image(self, data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=self.box_size,
            border=self.border,
        )
        print(len(data), data)
        qr.add_data(data)
        qr.make(fit=True)
        return qr.make_image()

    def get_base64_qr_data_uri(self):
        image_buffer = io.BytesIO()
        image = self._get_qr_image(self._get_active_card_uuid())
        image.save(image_buffer)
        base64_string = base64.b64encode(image_buffer.getvalue()).decode()
        return "data:image/png;base64,{0}".format(base64_string)
