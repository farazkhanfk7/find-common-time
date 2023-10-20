from rest_framework.response import Response
from rest_framework.views import APIView
from utils.utils import get_response_dict, convert_busy_slots_to_common_timezone, condition_assert, find_available_time_slots
from utils.services import get_user_timing_preferences_for_users
from rest_framework import status


class SuggestedTimeSlotsView(APIView):

    http_method_names = ['post']

    def post(self, request):
        try:
            user_ids = request.GET.get("users", "").split(",")
            duration = int(request.GET.get("duration_mins", 60))
            count = int(request.GET.get("count", 3))

            # Create a list of UserTimingPreference objects based on user_ids
            user_time_preferences = get_user_timing_preferences_for_users(user_ids=user_ids)

            # Convert busy slots to a common timezone
            calendar_data = request.data
            busy_slots = []       

            condition_assert(len(user_ids) == len(calendar_data), "Number of user ids and calendar data do not match")
            condition_assert(
                truth=all(
                    user_id in calendar_data for user_id in user_ids
                ),
                message="All user ids are not present in the calendar data"
            )

            for user_id in user_ids:
                busy_slots.append(convert_busy_slots_to_common_timezone(calendar_data[user_id]["calendars"]["primary"]["busy"]))

            slots = find_available_time_slots(
                user_time_preferences=user_time_preferences,
                busy_slots=busy_slots,
                duration=duration,
                count=count
            )

            return Response(
                get_response_dict(
                    message="Suggested time slots retrieved successfully",
                    data=slots
                ),
                status=status.HTTP_201_CREATED
            )
        
        except Exception as e:
            return Response(
                get_response_dict(
                    message="Suggested time slots retrieval failed",
                    error_details=str(e)
                ),
                status=status.HTTP_400_BAD_REQUEST
            )