from datetime import date

from servicebook.cars.models import CarInfo, CarTaxes, CarService


def create_cars_for_user(user, count=5):
    result = [CarInfo(
        brand=f'Brand{i + 1}',
        model=f'Model{i + 1}',
        year_of_manufacture=201+i,
        engine=f'2.{i + 1}',
        fuel=f"petrol",
        car_photo=f'https://cars.com/{i + 1}.jpg',
        user=user
    ) for i in range(count)]

    [p.save() for p in result]

    return result


def create_tax_for_user_and_car(user, car, count=5):
    taxes = [CarTaxes(
        type=f'Brand {i + 1}',
        valid_to=date(2023 + i, (1 + i) % 12, (1 + i) % 28),
        price=200+i,
        car=car,
        user=user,
    ) for i in range(count)]

    for tax in taxes:
        tax.save()

    return taxes


def create_service_for_user_and_car(user, car, count=5):
    services = [CarService(
        date_of_service=date(2023 + i, (1 + i) % 12, (1 + i) % 28),
        mileage=200000+i,
        symptoms=f"Symptom {i+1}",
        root_cause=f"Root cause {i + 1}",
        repair=f"Repair {i + 1}",
        price=200+i,
        car=car,
        user=user,
    ) for i in range(count)]

    for service in services:
        service.save()

    return services
