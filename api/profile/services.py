from typing import Any

from api.profile.serializers import ProfileDataSerializer, ProfileAvatarSerializer
from database.repositories import ProfileRepo
from helpers import Request


class ProfileService:
    @staticmethod
    def get_current_profile(request: Request) -> tuple[Any, str | None]:
        if not request.user.profile:
            return None, "Profile not found"

        serializer = ProfileDataSerializer(request.user.profile)
        return serializer.data, None

    @staticmethod
    def get_current_profile_avatar(request: Request) -> tuple[Any, str | None]:
        if not request.user.profile:
            return None, "Profile avatar not found"

        serializer = ProfileAvatarSerializer(request.user.profile)
        return serializer.data, None

    @staticmethod
    def update_profile(user_id: int | str, data: dict[str, Any]) -> tuple[Any, str | None]:
        name = data.get('name', None)
        bio = data.get('bio', None)
        address = data.get('address', None)

        profile = ProfileRepo.update_or_create_profile(user_id, name, bio, address)
        if not profile:
            return None, "Failed to update profile"

        serializer = ProfileDataSerializer(profile)
        return serializer.data, None

    @staticmethod
    def update_profile_avatar(user_id: int | str, avatar: Any) -> tuple[Any, str | None]:
        profile = ProfileRepo.get_profile_by_user_id(user_id)
        if not profile:
            profile = ProfileRepo.update_or_create_profile(user_id)
            if not profile:
                return None, "Failed to update profile avatar"

        profile = ProfileRepo.update_profile_avatar(profile.pk, avatar)
        serializer = ProfileAvatarSerializer(profile)
        return serializer.data, None
