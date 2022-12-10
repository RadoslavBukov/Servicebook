from servicebook.cars.models import CarInfo


def get_car_by_name_and_username(car_slug, user_id):
    return CarInfo.objects \
        .filter(slug=car_slug, user_id=user_id) \
        .get()
