from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from tests.accounts.BaseTestCase import TestCaseBase

UserModel = get_user_model()

class UserDetailsViewTests(TestCaseBase):
    VALID_USER_DATA = {
        'email': 'test_user@servicebook.tk',
        'password': '12345qwe',
    }

    def test_user_details__when_owner__expect_is_owner_true(self):
        user = self._create_user_and_login(self.VALID_USER_DATA)
        response = self.client.get(reverse_lazy('details user', kwargs={'pk': user.pk}))

        self.assertTrue(response.context['is_owner'])


    def test_user_details__when_not_owner__expect_is_owner_false(self):
        user = self._create_user_and_login({
            'email': self.VALID_USER_DATA['email'] + '1',
            'password': self.VALID_USER_DATA['password'],
        })

        self._create_user_and_login(self.VALID_USER_DATA)

        response = self.client.get(reverse_lazy('details user', kwargs={'pk': user.pk}))

        self.assertEqual(302, response.status_code)
        self.assertFalse(response.url == response.request['PATH_INFO'])

    def test_user_details__when_created__expect_empty_profile_info(self):
        user = self._create_user_and_login(self.VALID_USER_DATA)
        response = self.client.get(reverse_lazy('details user', kwargs={'pk': user.pk}))

        self.assertEqual('', response.context_data['full_name'])
        self.assertEqual(None, response.context_data['date_of_birth'])
        # self.assertEqual(ImageFieldFile, response.context_data['profile_picture'])


