from django.contrib.auth.hashers import make_password

import pytest
from faker import Faker

from users.factories import UserFactory

faker = Faker()

DUMMY_PASSWORD = 'Dummy#p455w07d'  # nosec


@pytest.fixture(scope='class')
def user(request):
    request.cls.user = UserFactory(password=make_password(DUMMY_PASSWORD))


@pytest.fixture(scope='class')
def inactive_user(request):
    request.cls.inactive_user = UserFactory(password=make_password(DUMMY_PASSWORD), is_active=False)


@pytest.fixture(scope='class')
def staff_user(request):
    request.cls.staff_user = UserFactory(password=make_password(DUMMY_PASSWORD), is_staff=True)


@pytest.fixture(scope='class')
def superuser(request):
    request.cls.superuser = UserFactory(password=make_password(DUMMY_PASSWORD), is_superuser=True)
