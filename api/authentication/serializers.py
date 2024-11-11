from rest_framework.serializers import (ModelSerializer,
                                        Serializer,
                                        CharField,
                                        DateTimeField,
                                        EmailField,
                                        FileField,
                                        IntegerField)

from database.models import User


class ValidateLoginPayload(Serializer):
    email = EmailField(max_length=50, required=True)
    password = CharField(required=True)


class ValidateVerifyOTPPayload(Serializer):
    email = EmailField(max_length=21, required=True)
    otp = IntegerField(required=True)


class ValidateCreateUserPayload(ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")


class ProfileDataSerializer(Serializer):
    oid = CharField(max_length=21, read_only=True)
    date_created = DateTimeField(read_only=True)
    date_updated = DateTimeField(read_only=True)
    date_deleted = DateTimeField(allow_null=True)
    name = CharField(max_length=50, allow_blank=True)
    phone = CharField(max_length=15, allow_blank=True)
    avatar = FileField(allow_null=True)


class UserDataSerializer(Serializer):
    oid = CharField(max_length=21, read_only=True)
    date_created = DateTimeField(read_only=True)
    date_updated = DateTimeField(read_only=True)
    date_deleted = DateTimeField(allow_null=True)
    email = CharField(max_length=50, required=True)
    last_login = DateTimeField(allow_null=True)
    profile = ProfileDataSerializer()
