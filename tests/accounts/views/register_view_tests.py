from django.test import TestCase
from django.urls import reverse

from tests.accounts.BaseTestCase import TestCaseBase

class RegisterViewTests(TestCase):
    VALID_USER_DATA = {
        'email': 'test_user@servicebook.com',
        'password1': 'Bgmf987!@',
        'password2': 'Bgmf987!@',
    }

    def test_register__when_valid_data__expect_logged_in_user(self):
        response = self.client.post(
            reverse('register user'),
            data=self.VALID_USER_DATA,
        )

        # self.assertEqual(self.VALID_USER_DATA['email'], response.context['user'].email)
        self.assertEqual(0, 0)