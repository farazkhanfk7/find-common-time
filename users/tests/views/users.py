from django.test import TestCase
from rest_framework.test import APIClient
from users.models import CustomUser

base_endpoint = "/users/"


class UserSignupTest(TestCase):
    def setUp(self):
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
        # signin with invalid password fails
        self.user_data["password"] = "random"
        response = self.client.post(base_endpoint + "signin/", data=self.user_data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["detail"], "User login failed")
        self.assertEqual(response.data["error_details"], "Invalid credentials")


class UpdateUserTest(TestCase):
    def setUp(self):
        self.user_data = {
            "email": "random@gmail.com",
            "password": "password123",
        }
        self.client = APIClient()

        # create user
        response = self.client.post(base_endpoint + "signup/", data=self.user_data)
        self.access_token = response.data["data"]["access"]

    def test_update_user(self):
        # checking if updating a user is successful
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.patch(
            base_endpoint + "update/",
            data={"name": "Random", "password": "password1234"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["detail"], "User updated successfully")
        self.assertEqual(response.data["data"]["name"], "Random")


class UserDetailTest(TestCase):
    def setUp(self):
        self.user_data = {"email": "random@gmail.com", "password": "password123"}

        self.client = APIClient()
        # create user
        response = self.client.post(base_endpoint + "signup/", data=self.user_data)

    def test_get_user_detail(self):
        # checking if getting user detail is successful
        user = CustomUser.objects.get(email=self.user_data["email"])
        response = self.client.get(base_endpoint + "detail/" + str(user.id) + "/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["detail"], "User details fetched successfully")
        self.assertEqual(response.data["data"]["name"], user.name)
        self.assertEqual(response.data["data"]["email"], user.email)
        self.assertEqual(response.data["data"]["id"], user.id)


class UserDeleteTest(TestCase):
    def setUp(self):
        self.user_data = {"email": "random@gmail.com", "password": "password123"}

        self.client = APIClient()

        response = self.client.post(base_endpoint + "signup/", data=self.user_data)
        self.access_token = response.data["data"]["access"]

    def test_delete_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.delete(base_endpoint + "delete/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["detail"], "User deleted successfully")
