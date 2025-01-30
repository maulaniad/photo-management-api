from rest_framework.serializers import ModelSerializer

from database.models import User, Profile


class ValidateCreateUser(ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "phone", "password"]


class ProfileDataSerializer(ModelSerializer):
    class Meta:
        model = Profile
        exclude = ["id"]


class UserDataSerializer(ModelSerializer):
    profile = ProfileDataSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "oid",
            "date_created",
            "date_updated",
            "date_deleted",
            "email",
            "phone",
            "last_login",
            "is_superuser",
            "profile",
            "groups",
            "user_permissions"
        ]
