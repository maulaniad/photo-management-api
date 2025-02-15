from typing import Any

from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password

from core.authentication import authenticate
from database.repositories import UserRepo
from helpers import Cache, Request
from helpers.types import EmailMessage
from helpers.utils import generate_token, generate_otp, send_email


class AuthService:
    @staticmethod
    def login(data: dict[str, Any]) -> tuple[str | Any, str | None]:
        email = data.get('email', None)
        password = data.get('password', None)

        user_data = authenticate(request=None, email=email, password=password)
        if not user_data:
            return None, "Invalid credentials"

        encoded_token = generate_token({'oid': user_data.oid})
        return encoded_token, None

    @staticmethod
    def refresh_token(request: Request) -> tuple[str | Any, str | None]:
        if not request.user.is_authenticated:
            return None, "User not authenticated"

        encoded_token = generate_token({'oid': request.user.oid})
        return encoded_token, None

    @staticmethod
    def create_otp(data: dict[str, Any]) -> tuple[bool, str | None]:
        email = data.get('email', None)
        otp_code = generate_otp()

        Cache().set(
            f"otp_{email}",
            {
                'otp': make_password(str(otp_code)),
                'retries': 0
            }
        )

        exp_min = settings.CACHES['default']['TIMEOUT'] // 60
        message = EmailMessage(
            subject="One Time Password - Django REST Framework",
            body=f"Your One Time Password is <b>{otp_code}</b>. Expires in {exp_min} minutes",
            to=[email],
        )
        send_email(message)
        return True, None

    @staticmethod
    def verify_otp(data: dict[str, Any]) -> tuple[str | Any, str | None]:
        email = data.get('email', None)
        otp_code = data.get('otp', None)
        cache = Cache()

        cached_data = cache.get(f"otp_{email}")
        if not cached_data:
            return None, "OTP has expired, please try again"

        if cached_data['retries'] >= settings.OTP_MAX_RETRIES:
            return None, "Max retries reached, please try login again"

        if not check_password(str(otp_code), cached_data['otp']):
            cached_data['retries'] += 1
            cache.set(f"otp_{email}", cached_data)
            return None, "Invalid One Time Password"

        cache.delete(f"otp_{email}")

        user_data = UserRepo.get_user_by_email(email=email)
        if not user_data:
            return None, "User is currently deactivated or does not exist"

        token = generate_token({'oid': user_data.oid})
        return token, None
