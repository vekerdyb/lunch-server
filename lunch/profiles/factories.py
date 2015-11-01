import factory
from lunch.profiles.models import Profile


class ProfileFactory(factory.DjangoModelFactory):
    class Meta:
        model = Profile