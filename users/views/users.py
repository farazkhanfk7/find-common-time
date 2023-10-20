from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.utils import get_response_dict
from users.services.users import sign_up_user, get_tokens_for_user
from users.selectors import get_user_by_email
from users.models import CustomUser
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import IntegrityError


class SignUpView(APIView):
    """
    Creates a new user.
    """

    http_method_names = ["post"]

    def post(self, request):
        try:
            email = request.data["email"]
            password = request.data["password"]

            user, jwt_tokens = sign_up_user(email, password)

            return Response(
                get_response_dict(message="User created successfully", data=jwt_tokens),
                status=status.HTTP_201_CREATED,
            )

        except IntegrityError as e:
            return Response(
                get_response_dict(message="User already exists", error_details=str(e)),
                status=status.HTTP_400_BAD_REQUEST,
            )


class SignInView(APIView):
    """
    Returns JWT tokens for a user.
    """

    http_method_names = ["post"]

    def post(self, request):
        try:
            email = request.data["email"]
            password = request.data["password"]

            user = get_user_by_email(email=email)
            if user.check_password(password):
                jwt_tokens = get_tokens_for_user(user)
                return Response(
                    get_response_dict(
                        message="User logged in successfully", data=jwt_tokens
                    ),
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    get_response_dict(
                        message="User login failed", error_details="Invalid credentials"
                    ),
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except CustomUser.DoesNotExist:
            return Response(
                get_response_dict(
                    message="User login failed", error_details="User does not exist"
                ),
                status=status.HTTP_401_UNAUTHORIZED,
            )


class UpdateUserView(APIView):
    """
    Updates a user.
    """

    http_method_names = ["patch"]
    permission_classes = [IsAuthenticated]

    class UserUpdateSerializer(serializers.ModelSerializer):
        class Meta:
            model = CustomUser
            fields = ["name", "password"]

    class UserUpdateOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = CustomUser
            fields = ["id", "name", "email"]

    def patch(self, request):
        user = request.user
        serializer = self.UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            # Get the current user
            user = request.user

            # Set the new password and save the user
            new_password = serializer.validated_data.pop("password")
            user.set_password(new_password)
            user.save()

            serializer.save()

            return Response(
                get_response_dict(
                    message="User updated successfully",
                    data=self.UserUpdateOutputSerializer(user).data,
                ),
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                get_response_dict(
                    message="User update failed", error_details=serializer.errors
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


class DeleteUserView(APIView):
    """
    Deletes a user.
    """

    http_method_names = ["delete"]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            user = request.user
            user.delete()
            return Response(
                get_response_dict(
                    message="User deleted successfully",
                ),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                get_response_dict(message="User deletion failed", error_details=str(e)),
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserDetailView(APIView):
    """
    Returns details of a user.
    """

    http_method_names = ["get"]
    permission_classes = [AllowAny]

    class UserDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = CustomUser
            fields = ["id", "name", "email"]

    def get(self, request, pk):
        try:
            user = CustomUser.objects.get(id=pk)
            serializer = self.UserDetailSerializer(user)
            return Response(
                get_response_dict(
                    message="User details fetched successfully", data=serializer.data
                ),
                status=status.HTTP_200_OK,
            )
        except CustomUser.DoesNotExist:
            return Response(
                get_response_dict(
                    message="User details fetch failed",
                    error_details="User does not exist",
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
