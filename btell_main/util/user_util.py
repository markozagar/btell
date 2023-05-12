import random
import itertools
import logging

from typing import Optional

from django import http
from django.contrib import auth
from django.contrib.auth import models as auth_models

def generate_random_password(length: int) -> str:
    """Generates a random, secure password of the given length."""

    a_to_z = [chr(c) for c in range(ord('a'), ord('z') + 1)]
    digits = [chr(c) for c in range(ord('0'), ord('9') + 1)]
    specials = ['!@#$%^&*_-']
    characters = list(itertools.chain(
        *a_to_z,
        *[c.upper() for c in a_to_z],
        *digits,
        *specials,
    ))
    password = [random.choice(characters) for _ in range(length)]
    return "".join(password)


def get_user_object(request: http.HttpRequest) -> Optional[auth_models.User]:
    """Retrieves the User object from the given request, if authenticated.

    This function will return `None` if the user is not authenticated, or if
    the model being used for `User` is not what we expect. In the latter
    case, a message will be logged.

    Args:
        request: The HttpRequest.
    
    Returns:
        Either a `User` object, or None if not authenticated.
    """
    if request.user.is_authenticated:
        if isinstance(request.user, auth_models.User):
            user: auth_models.User = request.user
            return user
        else:
            logging.warn("User model has the wrong type. Expected: '%s', found '%s'.",
                         auth_models.User._meta.object_name,
                         type(request.user))
        return None
