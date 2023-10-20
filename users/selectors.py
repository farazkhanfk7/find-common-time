from users.models import CustomUser, UserTimingPreference


def get_user_timing_preference(user_pk: int):
    return UserTimingPreference.objects.get(user=user_pk)


def get_user_by_email(email: str):
    return CustomUser.objects.get(email=email)
