from django.contrib.auth import models as auth_models
from django.db import models
import datetime

from servicebook.accounts.managers import AppUserManager
from servicebook.accounts.validators import validate_file_less_than_5mb, validate_date_is_not_in_future


class AppUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )
    date_joined = models.DateTimeField(
        default=datetime.datetime.now,
    )
    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'email'

    objects = AppUserManager()


class Profile(models.Model):
    first_name = models.CharField(
        max_length=25,
    )
    last_name = models.CharField(
        max_length=25,
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        validators=(validate_date_is_not_in_future,),
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=False,
        blank=True,
        validators=(validate_file_less_than_5mb,),
    )
    user = models.OneToOneField(
        AppUser,
        primary_key=True,
        on_delete=models.CASCADE,
    )


    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"

        return full_name.strip()

    def __str__(self):
        if not (self.first_name and self.last_name):
            return f" id: {self.user_id}"
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()
