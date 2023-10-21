import json
from datetime import datetime
from django.test import TestCase
from rest_framework.test import APIClient
from users.models import UserTimingPreference
from utils.utils import get_mock_data_for_busy_slots

base_endpoint = "/utils/suggested-times/"


class MeetingTimeSuggestionsTest(TestCase):
    def setUp(self):
        self.user_data1 = {
            "email": "user1@gmail.com",
            "password": "password123",
        }

        self.user_data2 = {
            "email": "user2@gmail.com",
            "password": "password123",
        }
        
        self.client = APIClient()
        # create user
        response_user1 = self.client.post("/users/signup/", data=self.user_data1)
        self.access_token_user1 = response_user1.data["data"]["access"]
        response_user2 = self.client.post("/users/signup/", data=self.user_data2)
        self.access_token_user2 = response_user2.data["data"]["access"]


        # update user time preferences
        preference_data = {
            "day_start_time": "08:00",
            "day_end_time": "17:00",
            "timezone": "Asia/Kolkata",
        }

        response1 = self.client.patch(
            "/users/time-preference/update/",
            data=preference_data,
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user1,
        )

        response2 = self.client.patch(
            "/users/time-preference/update/",
            data=preference_data,
            HTTP_AUTHORIZATION="Bearer " + self.access_token_user2,
        )

    def test_get_meeting_time_suggestions(self):

        user1 = UserTimingPreference.objects.get(user__email=self.user_data1["email"])
        user2 = UserTimingPreference.objects.get(user__email=self.user_data2["email"])
        busy_slots = get_mock_data_for_busy_slots([user1.id, user2.id])
        response = self.client.post(
            f"{base_endpoint}?users={user1.id},{user2.id}&duration_mins=60&count=3",
            data=busy_slots,
            format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data["detail"], "Suggested time slots retrieved successfully"
        )
        
        self.assertEqual(
            len(response.data["data"]), 3
        )

        current_date = datetime.today()
        current_date = current_date.strftime("%Y-%m-%d")
        success_data = [
            {
                'start': f"{current_date}T09:00:00+05:30",
                'end': f"{current_date}T10:00:00+05:30"
            },
            {
                'start': f"{current_date}T11:00:00+05:30",
                'end': f"{current_date}T12:00:00+05:30"
            },
            {
                'start': f"{current_date}T12:00:00+05:30",
                'end': f"{current_date}T13:00:00+05:30"
            }
        ]

        self.assertEqual(
            response.json()['data'],
            success_data
        )




