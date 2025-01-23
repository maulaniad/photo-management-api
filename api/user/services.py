from typing import Any

from django.contrib.auth.hashers import make_password
from django.db.models import QuerySet

from api.user.serializers import UserDataSerializer
from database.models.user import User
from database.repositories import UserRepo


class UserService:
    @staticmethod
    def get_users(lazy: bool = False) -> tuple[QuerySet[User, User] | Any, str | None]:
        user_data = UserRepo.get_users()

        if lazy:
            return user_data, None

        serializer = UserDataSerializer(user_data, many=True)
        return serializer.data, None

    @staticmethod
    def get_user(user_id: int | str) -> tuple[Any, str | None]:
        user_data = UserRepo.get_user(user_id)
        if not user_data:
            return None, "User not found"

        serializer = UserDataSerializer(user_data)
        return serializer.data, None

    @staticmethod
    def create_user(data: dict[str, Any]) -> tuple[Any, str | None]:
        email = data.get('email', None)
        password = data.get('password', None)

        user = UserRepo.create_user(
            email=email,
            password=make_password(password)
        )
        if not user:
            return None, "Failed to create user"

        serializer = UserDataSerializer(user)
        return serializer.data, None
