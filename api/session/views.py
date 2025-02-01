from django.db.models.query import QuerySet
from rest_framework.generics import ListCreateAPIView

from api.session.serializers import ValidateCreateSession, SessionDataSerializer
from api.session.services import SessionService
from core.authentication import JWTAuthentication
from helpers import HttpError, StandardPagination, Request, Response


class SessionView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = SessionDataSerializer
    pagination_class = StandardPagination
    service = SessionService

    def get_queryset(self) -> QuerySet:
        session_query, _ = self.service.get_sessions(lazy=True)
        return session_query.order_by('-date_created')

    def post(self, request: Request, *args, **kwargs):
        payload = ValidateCreateSession(data=request.data)

        if not payload.is_valid():
            raise HttpError._400_(payload.errors)

        session_data, error = self.service.create_session(**payload.data)
        if error:
            raise HttpError._500_(error)

        return Response(session_data, status=201, message="Session Created")
