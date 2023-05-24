from django.contrib.auth.hashers import make_password

import pytest

from documents.factories import DocumentFactory
from users.factories import UserFactory

DUMMY_PASSWORD = 'Dummy#p455w07d'  # nosec


@pytest.fixture(scope='class')
def user(request):
    request.cls.user = UserFactory(password=make_password(DUMMY_PASSWORD))


@pytest.fixture(scope='class')
def staff_user(request):
    request.cls.staff_user = UserFactory(password=make_password(DUMMY_PASSWORD), is_staff=True)


@pytest.fixture(scope='class')
def document(request):
    request.cls.document = DocumentFactory()
