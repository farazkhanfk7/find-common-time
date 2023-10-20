from django.test import TestCase
from rest_framework.test import APIClient
from users.models import CustomUser

base_endpoint = "/users/"


class UserTimePreferenceTest(TestCase):
    def setUp(self):
        self.user_data = {
            "email": "random@gmail.com",
            "password": "password123",
        }

        self.client = APIClient()
        # create user
        response = self.client.post(base_endpoint + "signup/", data=self.user_data)
        self.access_token = response.data["data"]["access"]

    def test_get_user_time_preference(self):
        self.user = CustomUser.objects.get(email=self.user_data["email"])
        response = self.client.get(
            base_endpoint + "time-preference/" + str(self.user.id) + "/detail/"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["detail"], "User time preference retrieved successfully"
        )
        self.assertEqual(response.data["data"]["day_start_time"], None)
        self.assertEqual(response.data["data"]["day_end_time"], None)
        self.assertEqual(response.data["data"]["timezone"], None)


class UpdateUserTimePreferenceTest(TestCase):
    def setUp(self):
        self.user_data = {"email": "random@gmail.com", "password": "password123"}

        self.client = APIClient()
        # create user
        response = self.client.post(base_endpoint + "signup/", data=self.user_data)
        self.access_token = response.data["data"]["access"]

    def test_update_user_time_preference(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.patch(
            base_endpoint + "time-preference/update/",
            data={
                "day_start_time": "10:00",
                "day_end_time": "20:00",
                "timezone": "Asia/Kolkata",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["detail"], "User time preference updated successfully"
        )
        self.assertEqual(response.data["data"]["day_start_time"], "10:00:00")
        self.assertEqual(response.data["data"]["day_end_time"], "20:00:00")
        self.assertEqual(response.data["data"]["timezone"], "Asia/Kolkata")
