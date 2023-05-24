import random

import factory
import pytest
from factory.django import DjangoModelFactory

from documents.models import Document
from users.factories import UserFactory

DUMMY_PASSWORD = 'Dummy#p455w07d'  # nosec


@pytest.mark.django_db
class DocumentFactory(DjangoModelFactory):
    class Meta:
        model = Document

    title = factory.Faker('word')
    content = factory.Faker('paragraphs', nb=random.randint(10, 50))  # nosec
    author = factory.SubFactory(UserFactory)
