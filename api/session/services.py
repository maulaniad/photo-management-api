from datetime import datetime
from typing import Any

from django.db.models import QuerySet

from api.session.serializers import SessionDataSerializer
from database.models import Session
from database.repositories import SessionRepo


class SessionService:
    @staticmethod
    def get_sessions(lazy: bool = False) -> tuple[QuerySet[Session, Session] | Any, str | None]:
        sessions = SessionRepo.get_sessions()

        if lazy:
            return sessions, None

        serializer = SessionDataSerializer(sessions, many=True)
        return serializer.data, None

    @staticmethod
    def create_session(session_code: str | None = None,
                       session_name: str | None = None,
                       date_taken: datetime | None = None) -> tuple[dict[str, Any] | Any, str | None]:
        session = SessionRepo.create_session(
            session_code=session_code,
            session_name=session_name,
            date_taken=date_taken
        )

        serializer = SessionDataSerializer(session)
        return serializer.data, None
