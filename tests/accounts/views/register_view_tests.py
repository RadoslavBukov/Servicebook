from django.test import TestCase
from django.urls import reverse


class RegisterViewTests(TestCase):
    VALID_USER_DATA = {
        'username': 'test_user@servicebook.com',
        'password1': 'Bgmf987!@',
        'password2': 'Bgmf987!@',
    }

    def test_register__when_valid_data__expect_logged_in_user(self):
        response = self.client.post(
            reverse('register user'),
            data=self.VALID_USER_DATA,
        )

        print(response.context['email'])

        self.assertEqual(self.VALID_USER_DATA['username'], response.context['user'].username)
