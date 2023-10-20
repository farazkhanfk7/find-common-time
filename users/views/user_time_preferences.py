from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from utils.utils import get_response_dict
from users.models import UserTimingPreference
from users.selectors import get_user_timing_preference


class UserTimePreferenceDetailView(APIView):
    """
    Returns user time preference.
    """

    http_method_names = ["get"]
    permission_classes = [IsAuthenticated]

    class UserTimePreferenceSerializer(serializers.ModelSerializer):
        class Meta:
            model = UserTimingPreference
            fields = ["day_start_time", "day_end_time", "timezone"]

    def get(self, request):
        try:
            user = request.user
            user_time_preference = get_user_timing_preference(user_pk=user.id)
            serializer = self.UserTimePreferenceSerializer(user_time_preference)
            return Response(
                get_response_dict(
                    message="User time preference retrieved successfully",
                    data=serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                get_response_dict(
                    message="User time preference retrieval failed",
                    error_details=str(e),
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


class UpdateUserTimePreferenceView(APIView):
    """
    Updates user time preference.
    """

    http_method_names = ["patch"]
    permission_classes = [IsAuthenticated]

    class UserTimePreferenceSerializer(serializers.ModelSerializer):
        class Meta:
            model = UserTimingPreference
            fields = ["day_start_time", "day_end_time", "timezone"]

    def patch(self, request):
        try:
            user = request.user
            user_time_preference = get_user_timing_preference(user_pk=user.id)
            serializer = self.UserTimePreferenceSerializer(
                user_time_preference, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    get_response_dict(
                        message="User time preference updated successfully",
                        data=serializer.data,
                    ),
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    get_response_dict(
                        message="User time preference update failed",
                        error_details=serializer.errors,
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                get_response_dict(
                    message="User time preference update failed", error_details=str(e)
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
