import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(
        lambda obj: "%s@example.com" % (obj.first_name.lower() + obj.last_name.lower())
    )
    username = factory.Faker("user_name")

    class Meta:
        model = get_user_model()
