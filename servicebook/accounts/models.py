from django.contrib.auth import models as auth_models
from django.db import models
from django.utils import timezone

from servicebook.accounts.managers import AppUserManager
from servicebook.accounts.validators import validate_file_less_than_5mb


class AppUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
    )
    is_staff = models.BooleanField(
        default=False,
        null=False,
        blank=False,
    )

    # User credentials consist of `email` and `password`
    USERNAME_FIELD = 'email'

    objects = AppUserManager()


class Profile(models.Model):
    first_name = models.CharField(
        max_length=25
    )
    last_name = models.CharField(
        max_length=25
    )
    profile_picture = models.ImageField(
        upload_to='profile_picture/',
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
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()
