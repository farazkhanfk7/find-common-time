from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils.utils import get_response_dict
from users.services.users import sign_up_user
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError


class SignUpView(APIView):
    """
    Creates a new user.
    """
    http_method_names = ['post']

    def post(self, request):
        try:
            email = request.data['email']
            password = request.data['password']

            user, jwt_tokens = sign_up_user(email, password)

            return Response(
                get_response_dict(
                    message="User created successfully",
                    data = jwt_tokens
                ),
                status=status.HTTP_201_CREATED
            )
        
        except IntegrityError as e:
            return Response(
                get_response_dict(
                    message="User already exists",
                    error_details=str(e)
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
        
