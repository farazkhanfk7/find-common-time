from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserTimingPreference, CustomUser


@receiver(post_save, sender=CustomUser)
def create_user_timing_preferences(sender, instance, created, **kwargs):
    if created:
        UserTimingPreference.objects.create(user=instance)
