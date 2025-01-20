from rest_framework.serializers import (ModelSerializer,
                                        Serializer,
                                        CharField,
                                        ImageField,
                                        ValidationError)

from database.models.profile import Profile


class ValidateUpdateProfile(Serializer):
    name = CharField(max_length=50, required=True)
    phone = CharField(max_length=16, required=False, allow_null=True)
    address = CharField(max_length=255, required=False, allow_null=True)


class ValidateUpdateProfileAvatar(Serializer):
    avatar = ImageField(required=True)
    
    def validate_avatar(self, value):
        if not value:
            raise ValidationError("An image is required.")

        if value.size > 5 * 1024 * 1024:
            raise ValidationError("Image size must not exceed 5MB.")

        if value.content_type not in ('image/jpeg', 'image/png'):
            raise ValidationError("Only JPEG and PNG images are allowed.")

        return value


class ProfileDataSerializer(ModelSerializer):
    class Meta:
        model = Profile
        exclude = ("id", "avatar")


class ProfileAvatarSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ("avatar",)
