from rest_framework.serializers import (Serializer,
                                        CharField,
                                        EmailField,
                                        IntegerField)


class ValidateLogin(Serializer):
    email = EmailField(max_length=50, required=True)
    password = CharField(required=True)


class ValidateVerifyOTP(Serializer):
    email = EmailField(max_length=21, required=True)
    otp = IntegerField(required=True)
