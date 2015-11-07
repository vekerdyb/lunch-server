import factory
from lunch.profiles.models import Profile


class ProfileFactory(factory.DjangoModelFactory):
    class Meta:
        model = Profile

    remote_system_id = factory.Sequence(lambda x: x)
