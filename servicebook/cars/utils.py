from servicebook.cars.models import CarInfo, CarTaxes, CarService


def get_car_by_slug_and_userid(car_slug, user_id):
    return CarInfo.objects \
        .filter(slug=car_slug, user_id=user_id) \
        .get()

def get_taxes_by_carid_and_userid(car_id, user_id):
    return CarTaxes.objects \
        .filter(car_id=car_id, user_id=user_id)

def get_tax_by_taxid(tax_id):
    return CarTaxes.objects \
        .filter(id=tax_id).get()

def get_services_by_carid_and_userid(car_id, user_id):
    return CarService.objects \
        .filter(car_id=car_id, user_id=user_id)

def get_service_by_serviceid(service_id):
    return CarService.objects \
        .filter(id=service_id).get()

def user_is_owner(request, user_id):
    return request.user.id == int(user_id)