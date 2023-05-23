from unittest.mock import patch

from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from utils.helpers import reverse_querystring


@pytest.mark.usefixtures('user', 'inactive_user')
class LoginViewTests(APITestCase):
    DUMMY_PASSWORD = 'Dummy#p455w07d'  # nosec

    @patch('users.serializers.update_last_login')
    def test_login_success(self, update_last_login_mock):
        url = reverse('auth:login')
        data = {
            'email': self.user.email,
            'password': self.DUMMY_PASSWORD,
        }
        response = self.client.post(url, data, format='json', secure=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        update_last_login_mock.assert_called_once()

    def test_login_bad_request(self):
        url = reverse('auth:login')
        data = {
            'username': self.user.email,
            'password': self.DUMMY_PASSWORD,
        }
        response = self.client.post(url, data, format='json', secure=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_unauthorized(self):
        url = reverse('auth:login')
        data = {
            'email': self.inactive_user.email,
            'password': self.DUMMY_PASSWORD,
        }
        response = self.client.post(url, data, format='json', secure=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_unsupported_media_type(self):
        url = reverse('auth:login')
        data = {
            'email': self.inactive_user.email,
            'password': self.DUMMY_PASSWORD,
        }
        response = self.client.post(url, data, secure=True)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


@pytest.mark.usefixtures('superuser', 'user', 'inactive_user')
class LoginAsViewTests(APITestCase):
    DUMMY_PASSWORD = 'Dummy#p455w07d'  # nosec

    def setUp(self):
        # Get access token for users.
        client = APIClient()
        url = reverse('auth:login')

        superuser_data = {
            'email': self.superuser.email,
            'password': self.DUMMY_PASSWORD
        }
        superuser_response = client.post(url, superuser_data, format='json', secure=True)
        superuser_access_token = superuser_response.data.get('access_token')
        self.superuser_access_token = superuser_access_token

        non_staff_data = {
            'email': self.user.email,
            'password': self.DUMMY_PASSWORD
        }
        non_staff_response = client.post(url, non_staff_data, format='json', secure=True)
        non_staff_access_token = non_staff_response.data.get('access_token')
        self.non_staff_access_token = non_staff_access_token

    def test_login_as_success(self):
        url = reverse_querystring('auth:login-as', query_kwargs={'id': self.user.pk})
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.superuser_access_token)
        response = client.post(url, format='json', secure=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_as_bad_request(self):
        url = reverse_querystring('auth:login-as')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.superuser_access_token)
        response = client.post(url, format='json', secure=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_as_forbidden(self):
        url = reverse_querystring('auth:login-as', query_kwargs={'id': self.superuser.pk})
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.non_staff_access_token)
        response = client.post(url, format='json', secure=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_as_not_found(self):
        url = reverse_querystring('auth:login-as', query_kwargs={'id': 12345})
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.superuser_access_token)
        response = client.post(url, format='json', secure=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


@pytest.mark.usefixtures('user')
class RefreshTokenViewTests(APITestCase):
    DUMMY_PASSWORD = 'Dummy#p455w07d'  # nosec

    def setUp(self):
        client = APIClient()
        url = reverse('auth:login')

        data = {
            'email': self.user.email,
            'password': self.DUMMY_PASSWORD
        }

        response = client.post(url, data, format='json', secure=True)

        access_token = response.data.get('access_token')
        refresh_token = response.data.get('refresh_token')

        self.access_token = access_token
        self.refresh_token = refresh_token

    def test_refresh_token_success(self):
        url = reverse('auth:refresh-token')
        client = APIClient()
        data = {
            'refresh': self.refresh_token
        }
        response = client.post(url, data, format='json', secure=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh_token_unauthorized(self):
        url = reverse('auth:refresh-token')
        client = APIClient()
        data = {
            'refresh': self.access_token
        }
        response = client.post(url, data, format='json', secure=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token_unsupported_media_type(self):
        url = reverse('auth:refresh-token')
        client = APIClient()
        data = {
            'refresh': self.access_token
        }
        response = client.post(url, data, secure=True)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


@pytest.mark.usefixtures('user')
class VerifyTokenViewTests(APITestCase):
    DUMMY_PASSWORD = 'Dummy#p455w07d'  # nosec

    def setUp(self):
        client = APIClient()
        url = reverse('auth:login')

        data = {
            'email': self.user.email,
            'password': self.DUMMY_PASSWORD
        }

        response = client.post(url, data, format='json', secure=True)

        access_token = response.data.get('access_token')
        refresh_token = response.data.get('refresh_token')

        self.access_token = access_token
        self.refresh_token = refresh_token

    def test_verify_token_success(self):
        url = reverse('auth:verify-token')
        client = APIClient()
        data = {
            'token': self.access_token
        }
        response = client.post(url, data, format='json', secure=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_token_bad_request(self):
        url = reverse('auth:verify-token')
        client = APIClient()
        data = {
            'access_token': self.refresh_token
        }
        response = client.post(url, data, format='json', secure=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_token_unsupported_media_type(self):
        url = reverse('auth:verify-token')
        client = APIClient()
        data = {
            'access_token': self.access_token
        }
        response = client.post(url, data, secure=True)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
