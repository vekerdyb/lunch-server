from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase

User = get_user_model()


class ProfileView(TestCase):
    credentials = {
        'username': 'user',
        'password': 'password'
    }

    def setUp(self):
        self.user = User.objects.create_user(**self.credentials)

    def test_should_return_base64_encoded_qr_code(self):
        self.client.login(**self.credentials)
        response = self.client.get(reverse('profile-me'))
        self.assertEqual(response.context['qr_code'][:22], 'data:image/png;base64,')
