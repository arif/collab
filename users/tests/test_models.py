from django.test import TestCase

import pytest


@pytest.mark.usefixtures('user')
class UserModelTest(TestCase):
    def test_str(self):
        expected_obj_name = f'{self.user.first_name} {self.user.last_name}'
        self.assertEqual(str(self.user), expected_obj_name)

    def test_get_full_name(self):
        expected_full_name = f'{self.user.first_name} {self.user.last_name}'
        self.assertEqual(self.user.get_full_name(), expected_full_name)

    def test_get_short_name(self):
        expected_short_name = f'{self.user.first_name}'
        self.assertEqual(self.user.get_short_name(), expected_short_name)

    def test_get_language(self):
        self.assertIsNotNone(self.user.get_language())
