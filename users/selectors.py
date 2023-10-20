from users.models import CustomUser, UserTimingPreference

def get_user_timing_preference(user):
    return UserTimingPreference.objects.get(user=user)

def get_user_by_email(email):
    return CustomUser.objects.get(email=email)