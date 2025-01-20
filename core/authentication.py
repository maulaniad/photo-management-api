from jwt import decode, ExpiredSignatureError, InvalidTokenError
from typing import Any, cast

from django.conf import settings
from django.contrib.auth import authenticate as _authenticate
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.http import HttpRequest
from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request

from database.models.user import User
from database.repositories import UserRepo
from helpers import HttpError


def authenticate(request: Request | None, **credentials) -> User | None:
    """Custom auth function. Doesn't change anything, only for type hinting."""
    return cast(User, _authenticate(request=request, **credentials))


class AuthenticationBackend(BaseBackend):
    repo = UserRepo

    def authenticate(self, request: HttpRequest, email=None, password=None, **kwargs):
        if not email or not password:
            raise HttpError._400_("Email and password are required to login")

        user_data = self.repo.manager().filter(email=email).select_related('profile').first()

        if not user_data:
            return None

        if not check_password(password, user_data.password):
            return None

        if not user_data.is_active:
            return None

        user_data.last_login = timezone.now()
        user_data.save()
        return user_data


class JWTAuthentication(BaseAuthentication):
    repo = UserRepo

    def authenticate(self, request: Request) -> tuple[Any, Any] | None:
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            raise HttpError._400_("No token provided")

        try:
            token = auth_header.split(" ")[1]
            payload = decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

            user = self.repo.get_user_by_email(email=payload['email'])
            if not user:
                raise HttpError._401_("User not registered")

            request.user = user
        except ExpiredSignatureError:
            raise HttpError._401_("Token expired")
        except (InvalidTokenError, KeyError):
            raise HttpError._400_("Invalid token")
        except IndexError:
            raise HttpError._400_("Invalid Bearer token format")

        return request.user, None
