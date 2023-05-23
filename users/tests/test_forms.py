from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

import pytest
from faker import Faker

from users import forms

UserModel = get_user_model()
fake = Faker()


class UserCreationFormTest(TestCase):
    DUMMY_PASSWORD = 'Dummy#p455w07d'  # nosec

    def test_clean_password_repeat(self):
        data = {
            'password': 'Dummy#p455w07d',
            'password_repeat': 'Dummy#p455w07d',
        }
        form = forms.UserCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_clean_password_repeat_not_valid(self):
        data = {
            'password': 'Dummy#p455w07d',
            'password_repeat': 'dummy#p455w07d',
        }
        form = forms.UserCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_save(self):
        data = {
            'email': fake.email(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'password': self.DUMMY_PASSWORD,
            'password_repeat': self.DUMMY_PASSWORD,
        }
        form = forms.UserCreationForm(data=data)
        user = form.save()
        self.assertIsInstance(user, UserModel)


@pytest.mark.usefixtures('user')
class UserChangeFormTest(TestCase):
    def test_clean_password(self):
        data = {
            'email': fake.email(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'language': settings.LANGUAGE_CODE,
        }
        form = forms.UserChangeForm(instance=self.user, data=data)
        self.assertTrue(form.is_valid())
