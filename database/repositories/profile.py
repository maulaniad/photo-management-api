from typing import Any

from django.db.models import Q
from django.db.transaction import atomic

from database.models.profile import Profile
from database.models.user import User


class ProfileRepo:
    @staticmethod
    def get_profiles():
        return Profile.objects.all()

    @staticmethod
    def get_profile(profile_id: int | str):
        return Profile.objects.filter(Q(id=profile_id) | Q(oid=profile_id)).first()

    @staticmethod
    def get_profile_by_user_id(user_id: int | str):
        return Profile.objects.filter(Q(user__id=user_id) | Q(user__oid=user_id)).first()

    @staticmethod
    def get_profile_by_email(email: str):
        return Profile.objects.filter(user_set__email=email).first()

    @staticmethod
    @atomic
    def update_or_create_profile(user_id: int | str,
                                 name: str | None = None,
                                 phone: str | None = None,
                                 address: str | None = None):
        user = User.objects.filter(
            Q(id=user_id) | Q(oid=user_id)
        ).select_related('profile').first()

        if not user:
            return None

        if not user.profile:
            profile = Profile.objects.create(
                name=name,
                phone=phone,
                address=address
            )
            user.profile = profile
            user.save()
            return profile

        user.profile.name = name if name else user.profile.name
        user.profile.phone = phone if phone else user.profile.phone
        user.profile.address = address if address else user.profile.address
        user.profile.save()
        return user.profile

    @staticmethod
    def update_profile_avatar(profile_id: int | str, avatar: Any):
        profile = Profile.objects.filter(Q(id=profile_id) | Q(oid=profile_id)).first()
        if not profile:
            return None

        profile.avatar = avatar
        profile.save()
        return profile

    @staticmethod
    def manager():
        return Profile.objects
