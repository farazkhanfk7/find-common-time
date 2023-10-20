from users.models import CustomUser
from ..utils.authentication import get_tokens_for_user
from typing import Tuple


def create_user_profile(email, password):
    user = CustomUser.objects.create_user(email, password)
    return user


def sign_up_user(email, password) -> Tuple[CustomUser, dict]:
    """
    Creates a new user and returns the user and tokens.
    """

    user = create_user_profile(email, password)
    jwt_tokens = get_tokens_for_user(user)
    return user, jwt_tokens

