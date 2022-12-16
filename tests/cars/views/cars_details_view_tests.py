from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from tests.accounts.BaseTestCase import TestCaseBase
from tests.utils.creation_utils import create_cars_for_user, create_tax_for_user_and_car, create_service_for_user_and_car

UserModel = get_user_model()


class UserDetailsViewTests(TestCaseBase):
    VALID_USER_DATA = {
        'email': 'test_user@servicebook.tk',
        'password': '12345qwe',
    }

    def test_my_cars_list__when_no_cars__expect_empty_cars(self):
        user = self._create_user_and_login(self.VALID_USER_DATA)
        response = self.client.get(reverse_lazy('cars list'))

        self.assertEqual(0, response.context['cars_count'])
        self.assertEqual(0, len(response.context['object_list']))

    def test_my_cars_list__when_3_car__expect_3_cars(self):
        user = self._create_user_and_login(self.VALID_USER_DATA)

        create_cars_for_user(user, count=3)

        response = self.client.get(reverse_lazy('cars list'))

        self.assertEqual(3, response.context['cars_count'])
        self.assertEqual(3, len(response.context['object_list']))


    def test_my_cars_list__when_5_cars_page_1__expect_3_cars_displayed(self):
        user = self._create_user_and_login(self.VALID_USER_DATA)

        cars = create_cars_for_user(user, count=5)

        response = self.client.get(
            reverse_lazy('cars list'),
            data={
                'page': 1,
            })

        self.assertEqual(3, len(response.context['object_list']))
        self.assertListEqual(cars[:3], list(response.context['object_list']))
        self.assertEqual(5, response.context['cars_count'])


    def test_my_cars_list__when_5_cars_page_2__expect_2_cars_displayed(self):
        user = self._create_user_and_login(self.VALID_USER_DATA)

        cars = create_cars_for_user(user, count=5)

        response = self.client.get(
            reverse_lazy('cars list'),
            data={
                'page': 2,
            })

        self.assertEqual(2, len(response.context['object_list']))
        self.assertListEqual(cars[3:], list(response.context['object_list']))
        self.assertEqual(5, response.context['cars_count'])


    def test_my_car_tax_details__when_car_created__expect_empty_tax(self):
        user = self._create_user_and_login(self.VALID_USER_DATA)

        car = create_cars_for_user(user, count=1)[0]

        response = self.client.get(reverse_lazy('taxes list', kwargs={
            'user_id': car.user_id,
            'car_slug': car.slug,
        }))

        self.assertEqual(0, len(response.context['taxes']))


    def test_my_car_tax_details__when_3_tax_created__expect_3_taxes(self):
        user = self._create_user_and_login(self.VALID_USER_DATA)

        car = create_cars_for_user(user, count=1)[0]
        taxes = create_tax_for_user_and_car(user, car, 3)

        response = self.client.get(reverse_lazy('taxes list', kwargs={
            'user_id': car.user_id,
            'car_slug': car.slug,
        }))

        self.assertEqual(3, len(response.context['taxes']))
        self.assertEqual(taxes, list(response.context['taxes']))


    def test_my_car_taxes_details__when_1_created_1_deleted__expect_empty_taxes(self):
        user = self._create_user_and_login(self.VALID_USER_DATA)

        car = create_cars_for_user(user, count=1)[0]
        taxes = create_service_for_user_and_car(user, car, 1)
        tax = taxes[0]
        tax.delete()

        response = self.client.get(reverse_lazy('services list', kwargs={
            'user_id': car.user_id,
            'car_slug': car.slug,
        }))

        self.assertEqual(0, len(response.context['services']))


    def test_my_car_service_details__when_car_created__expect_empty_service(self):
        user = self._create_user_and_login(self.VALID_USER_DATA)

        car = create_cars_for_user(user, count=1)[0]

        response = self.client.get(reverse_lazy('services list', kwargs={
            'user_id': car.user_id,
            'car_slug': car.slug,
        }))

        self.assertEqual(0, len(response.context['services']))


    def test_my_car_service_details__when_3_service_created__expect_3_service(self):
        user = self._create_user_and_login(self.VALID_USER_DATA)

        car = create_cars_for_user(user, count=1)[0]
        services = create_service_for_user_and_car(user, car, 3)

        response = self.client.get(reverse_lazy('services list', kwargs={
            'user_id': car.user_id,
            'car_slug': car.slug,
        }))

        self.assertEqual(3, len(response.context['services']))
        self.assertEqual(services, list(response.context['services']))


    def test_my_car_service_details__when_1_created_1_deleted__expect_empty_service(self):
        user = self._create_user_and_login(self.VALID_USER_DATA)

        car = create_cars_for_user(user, count=1)[0]
        services = create_service_for_user_and_car(user, car, 1)
        service = services[0]
        service.delete()

        response = self.client.get(reverse_lazy('services list', kwargs={
            'user_id': car.user_id,
            'car_slug': car.slug,
        }))

        self.assertEqual(0, len(response.context['services']))