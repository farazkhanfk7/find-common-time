import pytz
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserTimingPreference(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    # Make day_start_time and day_end_time nullable and allow blank values
    day_start_time = models.TimeField(null=True, blank=True)
    day_end_time = models.TimeField(null=True, blank=True)

    timezones = [(tz, tz) for tz in pytz.all_timezones]
    timezone = models.CharField(
        max_length=100, choices=timezones, null=True, blank=True
    )

    def __str__(self):
        return f"Timing Preferences for {self.user.email}"

    class Meta:
        verbose_name_plural = "User Timing Preferences"
