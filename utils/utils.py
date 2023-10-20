import pytz
from django.utils import timezone
from typing import Union, List
from datetime import timedelta, datetime
from users.models import UserTimingPreference
from utils.exceptions import ConditionFailedException
from users.selectors import get_user_timing_preference

def get_response_dict( message: str, data : Union[list, dict] = None, error_details=None) -> dict:
    """
    Returns a dictionary with the given message and data
    """
    return {
        "detail": message,
        "data": data,
        "error_details": error_details
    }


def condition_assert(truth, message):
    if not truth:
        raise ConditionFailedException(message)


def convert_busy_slots_to_common_timezone(busy_slots):

    common_timezone = timezone.get_current_timezone()
    converted_busy_slots = []
    for slot in busy_slots:
        # convert start time to common timezone
        start_time = datetime.strptime(slot["start"], "%Y-%m-%dT%H:%M:%S%z").astimezone(common_timezone)
        # convert end time to common timezone
        end_time = datetime.strptime(slot["end"], "%Y-%m-%dT%H:%M:%S%z").astimezone(common_timezone)

        converted_busy_slots.append({"start": start_time, "end": end_time})

    return converted_busy_slots


def find_available_time_slots(user_time_preferences, busy_slots, duration, count):
    # Get the common start and end times for user preferences
    common_timezone = timezone.get_current_timezone()
    start_times = []
    for user in user_time_preferences:
        # Convert user's start time to common timezone

        # Note: I am using busy_slots[0][0]["start"] to get the same date as the busy slot
        # assuming that all users have the same date for their busy slots and that the busy slots
        # are of the same date
        user_timezone = pytz.timezone(user.timezone)
        start_times.append(user_timezone.localize((datetime.combine(busy_slots[0][0]["start"], user.day_start_time))).astimezone(common_timezone))

    end_times = []
    for user in user_time_preferences:
        user_timezone = pytz.timezone(user.timezone)
        end_times.append(user_timezone.localize(datetime.combine(busy_slots[0][0]["end"], user.day_end_time)).astimezone(common_timezone))

    common_start_time = max(start_times)
    common_end_time = min(end_times)

    print(common_start_time)
    print(common_end_time)

    suggested_slots = []

    current_time = common_start_time

    while current_time + timedelta(minutes=duration) <= common_end_time and len(suggested_slots) < count:
        slot_valid = True

        for i in range(len(user_time_preferences)):
            for busy_slot in busy_slots[i]:
                busy_start_time = busy_slot["start"]
                busy_end_time = busy_slot["end"]

                if current_time + timedelta(minutes=duration) <= busy_start_time or current_time >= busy_end_time:
                    continue
                else:
                    slot_valid = False
                    break

            if not slot_valid:
                break  # No need to check other users

        if slot_valid:
            end_time = current_time + timedelta(minutes=duration)
            suggested_slots.append({"start": current_time, "end": end_time})
            current_time += timedelta(minutes=duration)
        else:
            current_time += timedelta(minutes=duration)

    return suggested_slots

