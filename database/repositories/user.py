from django.db.models import Q

from database.models import User


class UserRepo:
    @staticmethod
    def get_users():
        return User.objects.all().select_related('profile')

    @staticmethod
    def get_user(user_id: int | str):
        return User.objects.filter(
            Q(id=user_id) | Q(oid=user_id)
        ).select_related('profile').first()

    @staticmethod
    def get_user_by_email(email: str):
        return User.objects.filter(
            email=email
        ).select_related('profile').first()

    @staticmethod
    def get_user_by_phone(phone: str):
        return User.objects.filter(
            phone=phone
        ).select_related('profile').first()

    @staticmethod
    def create_user(email: str, password: str, phone: str | None = None, is_superuser: bool = False):
        return User.objects.create(
            email=email,
            phone=phone,
            password=password,
            is_superuser=is_superuser,
        )

    @staticmethod
    def manager():
        return User.objects
