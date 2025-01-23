from django.conf import settings
from rest_framework.generics import GenericAPIView

from api.authentication.serializers import ValidateLogin, ValidateVerifyOTP
from api.authentication.services import AuthService
from core.authentication import JWTAuthentication
from helpers import HttpError, Request, Response


class LoginView(GenericAPIView):
    service = AuthService

    def post(self, request: Request, *args, **kwargs):
        payload = ValidateLogin(data=request.data)

        if not payload.is_valid():
            raise HttpError._400_(payload.errors)

        token, error = self.service.login(payload.data)
        if error:
            raise HttpError._401_(error)

        if settings.OTP_AUTH:
            self.service.create_otp(payload.data)
            return Response(None, message="OTP has been sent to your email")

        return Response({'token': token}, message="Authenticated")


class RefreshTokenView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    service = AuthService

    def get(self, request: Request, *args, **kwargs):
        token, error = self.service.refresh_token(request)
        if error:
            raise HttpError._401_(error)

        return Response({'token': token}, message="Token Refreshed")


class VerifyOTPView(GenericAPIView):
    service = AuthService

    def post(self, request: Request, *args, **kwargs):
        payload = ValidateVerifyOTP(data=request.data)

        if not payload.is_valid():
            raise HttpError._400_(payload.errors)

        token, error = self.service.verify_otp(data=payload.data)
        if error:
            raise HttpError._401_(error)

        return Response({'token': token}, message="OTP Verified")
