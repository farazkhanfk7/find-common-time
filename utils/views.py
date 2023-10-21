from rest_framework.response import Response
from rest_framework.views import APIView
from utils.utils import (
    get_response_dict,
    convert_busy_slots_to_common_timezone,
    condition_assert,
    find_available_time_slots,
)
from utils.exceptions import ConditionFailedException
from utils.selectors import get_user_timing_preferences_for_users
from rest_framework import status


class SuggestedTimeSlotsAPIView(APIView):
    """
    API view for suggesting time slots.
    """

    http_method_names = ["post"]

    def post(self, request):
        try:
            # extract input parameters
            user_ids = request.GET.get("users", "").split(",")
            duration = int(request.GET.get("duration_mins", 60))
            count = int(request.GET.get("count", 3))

            if not user_ids:
                return Response(
                    get_response_dict("Suggested time slots retrieval failed", data=None, error_details="No user IDs provided"),
                    status=status.HTTP_400_BAD_REQUEST
                )

            # fetch user time preferences
            user_time_preferences = get_user_timing_preferences_for_users(user_ids=user_ids)

            calendar_data = request.data
            busy_slots = []

            # validate user ids and calendar data
            if len(user_ids) != len(calendar_data):
                return Response(
                    get_response_dict("Suggested time slots retrieval failed", data=None, error_details="Number of user IDs and calendar data do not match"),
                    status=status.HTTP_400_BAD_REQUEST
                )
            for user_id in user_ids:
                if user_id not in calendar_data:
                    return Response(
                        get_response_dict("Suggested time slots retrieval failed", data=None, error_details=f"Calendar data for user {user_id} not provided"),
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # convert busy slots to a common timezone
                busy_slots.append(
                    convert_busy_slots_to_common_timezone(calendar_data[user_id]["calendars"]["primary"]["busy"])
                )

            # find available time slots
            slots = find_available_time_slots(
                user_time_preferences=user_time_preferences,
                busy_slots=busy_slots,
                duration=duration,
                count=count,
            )

            return Response(
                get_response_dict("Suggested time slots retrieved successfully", data=slots, error_details=None),
                status=status.HTTP_201_CREATED,
            )

        except ConditionFailedException as e:
            return Response(
                get_response_dict("Suggested time slots retrieval failed", data=None, error_details=str(e)),
                status=status.HTTP_400_BAD_REQUEST,
            )