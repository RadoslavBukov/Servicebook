from django.contrib.auth import get_user_model
from django.db.models import signals
from django.dispatch import receiver

from servicebook.cars.models import CarTaxes, CarService, CarInfo
from servicebook.cars.utils import get_taxes_by_carid_and_userid

UserModel = get_user_model()


# Todo: Update field days_to_expire in CarService model with change of the date
# @receiver(signals.post_init, sender=CarTaxes)
# def update_tax_daystoexpire_with_datechange(car_id, user_id, *args, **kwargs):
#
#     taxes = get_taxes_by_carid_and_userid(car_id, user_id)
#
#     for tax in taxes:
#         tax.save()