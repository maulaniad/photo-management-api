from datetime import datetime

from django.db.models import Q, Count

from database.models import Session


class SessionRepo:
    @staticmethod
    def get_sessions():
        return Session.objects.annotate(
            total_photos=Count('photo')
        ).all()

    @staticmethod
    def get_session_by_id(session_id: int | str):
        return Session.objects.filter(
            Q(id=session_id) if isinstance(session_id, int) else Q(oid=session_id)
        ).annotate(total_photos=Count('photo')).first()

    @staticmethod
    def get_session_by_code(session_code: str):
        return Session.objects.filter(session_code=session_code).annotate(
            total_photos=Count('photo')
        ).first()

    @staticmethod
    def create_session(session_code: str, session_name: str | None = None, date_taken: datetime | None = None):
        return Session.objects.create(
            date_taken=date_taken,
            session_code=session_code,
            session_name=session_name
        )

    @staticmethod
    def manager():
        return Session.objects
