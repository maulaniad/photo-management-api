from rest_framework.generics import GenericAPIView

from core.authentication import JWTAuthentication
from api.profile.services import ProfileService
from api.profile.serializers import ValidateUpdateProfile, ValidateUpdateProfileAvatar
from helpers import HttpError, Request, Response


class ProfileView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    service = ProfileService

    def get(self, request: Request, *args, **kwargs):
        profile_data, error = self.service.get_current_profile(request)
        if error:
            raise HttpError._404_(error)

        return Response(profile_data)

    def put(self, request: Request, *args, **kwargs):
        payload = ValidateUpdateProfile(data=request.data)

        if not payload.is_valid():
            raise HttpError._400_(payload.errors)

        profile_data, error = self.service.update_profile(request.user.pk, payload.data)
        if error:
            raise HttpError._500_(error)

        return Response(profile_data)


class ProfileAvatarView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    service = ProfileService

    def get(self, request: Request, *args, **kwargs):
        avatar, error = self.service.get_current_profile_avatar(request)
        if error:
            raise HttpError._404_(error)

        return Response(avatar)

    def put(self, request: Request, *args, **kwargs):
        payload = ValidateUpdateProfileAvatar(data=request.FILES)

        if not payload.is_valid():
            raise HttpError._400_(payload.errors)

        profile_data, error = self.service.update_profile_avatar(
            request.user.pk, request.FILES.get('avatar')
        )
        if error:
            raise HttpError._500_(error)

        return Response(profile_data)
