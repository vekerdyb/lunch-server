from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase
from lunch.cards.models import Card
from lunch.profiles.factories import ProfileFactory

User = get_user_model()


class ProfileView(TestCase):
    credentials = {
        'username': 'user',
        'password': 'password'
    }

    def test_should_return_base64_encoded_qr_code(self):
        self.user = User.objects.create_user(**self.credentials)
        self.profile = ProfileFactory(user=self.user)
        self.assertEqual(Card.objects.count(), 1)
        self.client.login(**self.credentials)
        response = self.client.get(reverse('profile-me'))
        self.assertEqual(response.context['qr_code'][:22], 'data:image/png;base64,')


class ProfileModel(TestCase):
    def test_should_create_card_when_creating_profile(self):
        self.profile = ProfileFactory()
        self.assertEqual(Card.objects.count(), 1)
