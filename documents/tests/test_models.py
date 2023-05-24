from django.test import TestCase

import pytest


@pytest.mark.usefixtures('document')
class DocumentModelTests(TestCase):
    def test_str(self):
        value = self.document.title
        self.assertEquals(str(self.document), value)
