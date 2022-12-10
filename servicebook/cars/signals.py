from django.contrib.auth import get_user_model
from django.db.models import signals
from django.dispatch import receiver

from servicebook.cars.models import CarTaxes, CarService, CarInfo

UserModel = get_user_model()


@receiver(signals.post_save, sender=CarInfo)
def create_cartaxes_and_carservice_on_car_created(instance, created, *args, **kwargs):
    if not created:
        return

    CarTaxes.objects.create(
        car_id=instance.pk,
    )

    CarService.objects.create(
        car_id=instance.pk,
    )