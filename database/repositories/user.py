from django.db.models import Q

from database.models import User


class UserRepo:
    @staticmethod
    def get_users():
        return User.objects.all().select_related('profile')

    @staticmethod
    def get_user(id_or_oid: int | str) -> User | None:
        return User.objects.filter(
            Q(id=id_or_oid) | Q(oid=id_or_oid)
        ).select_related('profile').first()

    @staticmethod
    def get_user_by_email(email: str) -> User | None:
        return User.objects.filter(
            email=email
        ).select_related('profile').first()

    @staticmethod
    def create_user(email: str, password: str, is_superuser: bool = False) -> User:
        return User.objects.create(
            email=email,
            password=password,
            is_superuser=is_superuser,
        )

    @staticmethod
    def manager():
        return User.objects
