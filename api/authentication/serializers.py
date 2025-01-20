from rest_framework.serializers import (ModelSerializer,
                                        Serializer,
                                        CharField,
                                        DateTimeField,
                                        EmailField,
                                        FileField,
                                        IntegerField)

from database.models.user import User


class ValidateLogin(Serializer):
    email = EmailField(max_length=50, required=True)
    password = CharField(required=True)


class ValidateVerifyOTP(Serializer):
    email = EmailField(max_length=21, required=True)
    otp = IntegerField(required=True)


class ValidateCreateUser(ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")


class ProfileDataSerializer(Serializer):
    oid = CharField(max_length=21, read_only=True)
    name = CharField(max_length=50, allow_blank=True)
    phone = CharField(max_length=15, allow_blank=True)
    avatar = FileField(allow_null=True)


class UserDataSerializer(Serializer):
    oid = CharField(max_length=21, read_only=True)
    email = CharField(max_length=50, required=True)
    last_login = DateTimeField(allow_null=True)
    profile = ProfileDataSerializer()
