from django.contrib.auth.hashers import make_password
from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.test import APITestCase

DUMMY_PASSWORD = 'Dummy#p455w07d'  # nosec


@pytest.mark.usefixtures('document', 'user')
class DocumentViewSetTests(APITestCase):
    def setUp(self):
        url = reverse('auth:login')

        user_data = {
            'email': self.user.email,
            'password': DUMMY_PASSWORD,
        }
        user_response = self.client.post(url, user_data, format='json', secure=True)
        user_access_token = user_response.data.get('access_token')
        self.USER_CREDENTIALS = {
            'HTTP_AUTHORIZATION': f'Bearer {user_access_token}'
        }

        self.document.author.password = make_password(DUMMY_PASSWORD)
        self.document.author.save()

        document_user_data = {
            'email': self.document.author.email,
            'password': DUMMY_PASSWORD,
        }
        document_user_response = self.client.post(url, document_user_data, format='json', secure=True)
        document_user_access_token = document_user_response.data.get('access_token')
        self.DOCUMENT_USER_CREDENTIALS = {
            'HTTP_AUTHORIZATION': f'Bearer {document_user_access_token}'
        }

    def test_list_documents(self):
        url = reverse('document:documents-list')
        self.client.credentials(**self.DOCUMENT_USER_CREDENTIALS)
        response = self.client.get(url, format='json', secure=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
