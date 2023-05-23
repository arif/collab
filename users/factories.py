from django.contrib.auth import get_user_model

from factory import Faker
from factory.django import DjangoModelFactory

UserModel = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = UserModel
        django_get_or_create = ('email', )

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('email')
