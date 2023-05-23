from django.contrib.auth import get_user_model
from django.test import TestCase

from faker import Faker

UserModel = get_user_model()

fake = Faker()


class UserManagerTest(TestCase):
    DUMMY_PASSWORD = 'Dummy#p455w07d'  # nosec

    def test_create_user_success(self):
        data = {
            'email': fake.email(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'password': self.DUMMY_PASSWORD,
        }

        user = UserModel.objects.create_user(**data)
        self.assertIsInstance(user, UserModel)

    def test_create_user_no_email(self):
        data = {
            'email': None,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'password': self.DUMMY_PASSWORD,
        }

        with self.assertRaises(ValueError):
            UserModel.objects.create_user(**data)

    def test_create_user_no_password(self):
        data = {
            'email': fake.email(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'password': None,
        }

        with self.assertRaises(ValueError):
            UserModel.objects.create_user(**data)

    def test_create_user_no_first_or_last_name(self):
        data = {
            'email': fake.email(),
            'first_name': fake.first_name(),
            'last_name': None,
            'password': self.DUMMY_PASSWORD,
        }

        with self.assertRaises(ValueError):
            UserModel.objects.create_user(**data)

    def test_create_superuser_success(self):
        data = {
            'email': fake.email(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'password': self.DUMMY_PASSWORD,
        }

        user = UserModel.objects.create_superuser(**data)
        self.assertIsInstance(user, UserModel)
