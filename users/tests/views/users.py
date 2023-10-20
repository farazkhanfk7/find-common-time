from django.test import TestCase
from rest_framework.test import APIClient
from users.models import CustomUser

base_endpoint = "/users/"


class UserSignupTest(TestCase):
    def setUp(self):
        # Create a test user for your setup
        self.user_data = {
            "email": "test@example.com",
            "password": "password123",
        }
        self.client = APIClient()

    def test_signup(self):
        response = self.client.post(base_endpoint + "signup/", data=self.user_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["detail"], "User created successfully")

    def test_signup_existing_user(self):
        # Ensure creating a user with an existing email fails
        self.client.post(base_endpoint + "signup/", data=self.user_data)
        response = self.client.post(base_endpoint + "signup/", data=self.user_data)
        self.assertEqual(response.status_code, 400)


class UserSigninTest(TestCase):
    def setUp(self):
        # Create a test user for your setup
        self.user_data = {
            "email": "random@gmail.com",
            "password": "password123",
        }
        self.client = APIClient()
        self.client.post(base_endpoint + "signup/", data=self.user_data)

    def test_signin(self):
        response = self.client.post(base_endpoint + "signin/", data=self.user_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["detail"], "User logged in successfully")

    def test_signin_invalid_password(self):
        # Ensure signin with invalid password fails
        self.user_data["password"] = "random"
        response = self.client.post(base_endpoint + "signin/", data=self.user_data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "User login failed")
        self.assertEqual(response.data["error_details"], "Invalid credentials")
