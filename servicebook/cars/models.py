from django.contrib.auth import models as auth_models, get_user_model
from datetime import date
from django.db import models
from enum import Enum
from django.utils.text import slugify

from servicebook.accounts.models import AppUser
from servicebook.accounts.validators import validate_file_less_than_5mb, validate_date_is_not_in_future
from servicebook.cars.validators import validate_string_min_2_symbols, validate_year_between_1970_and_2022, \
    validate_date_is_not_in_past
from servicebook.core.model_mixins import ChoicesEnumMixin

UserModel = get_user_model()

class CarBrand(ChoicesEnumMixin, Enum):
    AUDI = 'Audi'
    BMW = "BMW"
    Ford = "Ford"
    VW = "Volkswagen"
    HONDA = "Honda"
    MAZDA = "Mazda"
    MERCEDES = "Mercedes"
    MITSUBISHI = "Mitsubishi"
    TOYOTA = "Toyota"
    SUBARU = "Subaru"
    SUZUKI = "Suzuki"
    JEEP = "Jeep"
    OPEL = "Opel"
    NISSAN = "Nissan"
    RENAULT = "Renault"
    Other = "Other"


class CarTaxes(ChoicesEnumMixin, Enum):
    INSURANCE = 'Insurance'
    INSPECTION = "Inspection"
    TAX = "Tax"
    VIGNETTE = "Vignette"
    Other = "Other"


class CarInfo(models.Model):
    MAX_LEN_MODEL = 20
    MAX_LEN_CHARFIELD = 20

    brand = models.CharField(
        max_length=MAX_LEN_CHARFIELD,
        choices=CarBrand.choices(),
        null=False,
        blank=False,
    )
    model = models.CharField(
        max_length=MAX_LEN_MODEL,
        null=False,
        blank=False,
        validators=(
            validate_string_min_2_symbols,
        ),
    )
    year_of_manufacture = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=(
            validate_year_between_1970_and_2022,
        ),
    )
    engine = models.CharField(
        max_length=MAX_LEN_CHARFIELD,
        null=True,
        blank=True,
    )
    fuel = models.CharField(
        max_length=MAX_LEN_CHARFIELD,
        null=True,
        blank=True,
    )
    car_photo = models.URLField(
        null=True,
        blank=True,
    )
    slug = models.SlugField(
        unique=True,
        null=False,
        blank=True,
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT,
    )

    # def __str__(self):
    #     if not (self.brand and self.model):
    #         return f" id: {self.user_id}"
    #     brand_model = "%s %s" % (self.brand, self.model)
    #     return brand_model.strip()

    def save(self, *args, **kwargs):
        # Create/Update
        super().save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(f'{self.id}-{self.model}')

        # Without the `if` the following scenario might happen:
        # The url is `/pets/4-stamat`
        # Rename `stamat` to `stamata`
        # The new url is `/pets/4-stamata`, but `/pets/4-stamat` does not work

        # Update
        return super().save(*args, **kwargs)

class CarTaxes(models.Model):
    MAX_LEN_MODEL = 20
    MAX_LEN_CHARFIELD = 20

    type = models.CharField(
        max_length=MAX_LEN_CHARFIELD,
        choices=CarTaxes.choices(),
        null=True,
        blank=True,
    )
    valid_to = models.DateField(
        null=True,
        blank=True,
        validators=(
            validate_date_is_not_in_past,
        ),
    )
    days_to_expiry = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    price = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    car = models.ForeignKey(
        CarInfo,
        on_delete=models.RESTRICT,
    )


class CarService(models.Model):
    MAX_LEN_CHARFIELD = 20

    date_of_service = models.DateField(
        null=True,
        blank=True,
        validators=(
            validate_date_is_not_in_future,
        ),
    )
    mileage = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    symptoms = models.CharField(
        max_length=MAX_LEN_CHARFIELD,
        null=True,
        blank=True,
    )
    root_cause = models.CharField(
        max_length=MAX_LEN_CHARFIELD,
        null=True,
        blank=True,
    )
    repair = models.CharField(
        max_length=MAX_LEN_CHARFIELD,
        null=True,
        blank=True,
    )
    price = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    car = models.ForeignKey(
        CarInfo,
        on_delete=models.RESTRICT,
    )

