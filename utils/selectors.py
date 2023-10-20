from typing import List
from utils.utils import condition_assert
from users.models import UserTimingPreference
from utils.exceptions import ConditionFailedException
from users.selectors import get_user_timing_preference


def get_user_timing_preferences_for_users(
    user_ids: List[int],
) -> List[UserTimingPreference]:
    """
    Returns a list of UserTimingPreference objects for the given user ids
    """
    user_timing_preferences = []
    for user_id in user_ids:
        try:
            utp_obj = get_user_timing_preference(user_pk=user_id)
            condition_assert(
                utp_obj.day_start_time is not None
                and utp_obj.day_end_time is not None
                and utp_obj.timezone is not None,
                f"UserTimingPreference for user_id: {user_id} does not have all required fields",
            )
            user_timing_preferences.append(utp_obj)
        except UserTimingPreference.DoesNotExist:
            # Handle cases where the UserTimingPreference does not exist for the user
            raise ConditionFailedException(
                f"UserTimingPreference does not exist for user with id: {user_id}"
            )

    return user_timing_preferences
