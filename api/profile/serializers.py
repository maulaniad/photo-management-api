from rest_framework.serializers import ModelSerializer, Serializer, ImageField

from database.models import Profile
from helpers.exception import ValidationError


class ValidateUpdateProfile(ModelSerializer):
    class Meta:
        model = Profile
        depth = 0
        fields = ["name", "bio", "address"]


class ValidateUpdateProfileAvatar(Serializer):
    avatar = ImageField(required=True)
    
    def validate_avatar(self, value):
        if not value:
            raise ValidationError("An image is required.")

        if value.size > 5 * 1024 * 1024:
            raise ValidationError("Image size must not exceed 5MB.")

        if value.content_type not in ["image/jpeg", "image/jpg", "image/png", "image/webp"]:
            raise ValidationError("Only JPEG, PNG and WEBP images are allowed.")

        return value


class ProfileDataSerializer(ModelSerializer):
    class Meta:
        model = Profile
        depth = 0
        exclude = ["id", "avatar"]


class ProfileAvatarSerializer(ModelSerializer):
    class Meta:
        model = Profile
        depth = 0
        fields = ["avatar"]
