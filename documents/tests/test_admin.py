from django.contrib.admin import site
from django.test import RequestFactory, TestCase

import pytest

from documents import admin, models


@pytest.mark.usefixtures('staff_user')
class DocumentAdminTests(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.admin = admin.DocumentAdmin(models.Document, site)

    def test_save_model(self):
        request = self.request_factory.get('/')
        request.user = self.staff_user

        self.document = models.Document(title='Test', content='Test document content.')

        form = self.admin.get_form(request)()

        self.admin.save_model(request=request, obj=self.document, form=form, change=False)

        self.document.refresh_from_db()

        self.assertIsNotNone(self.document.author)
        self.assertEqual(self.document.author, self.staff_user)
