from rest_framework.generics import GenericAPIView, ListCreateAPIView

from api.user.serializers import UserDataSerializer, ValidateCreateUser
from api.user.services import UserService
from core.authentication import JWTAuthentication
from helpers import HttpError, Request, Response, StandardPagination


class UserView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    pagination_class = StandardPagination
    serializer_class = UserDataSerializer
    service = UserService

    def get_queryset(self):
        user_query, _ = self.service.get_users(lazy=True)
        return user_query.order_by('-date_created')

    def post(self, request: Request, *args, **kwargs) -> Response:
        payload = ValidateCreateUser(data=request.data)

        if not payload.is_valid():
            raise HttpError._400_(payload.errors)

        _, error = self.service.create_user(data=payload.data)
        if error:
            raise HttpError._500_(error)

        return Response(None, message="User Created")


class UserDetailView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    service = UserService

    def get(self, request: Request, id: str) -> Response:
        user_data, error = self.service.get_user(id)
        if error:
            raise HttpError._404_(error)

        return Response(user_data)
