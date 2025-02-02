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
    def create_session(session_code: str | None = None, session_name: str | None = None, date_taken: datetime | None = None):
        # TODO: Refactor, seperate validation from repository
        # This code requires refactoring, currently it intercepts all optional values
        # so that Django ORM wouldn't think it gives null/None value
        # and will fire the default function from the model instead
        data_dict = {}

        if session_code:
            data_dict['session_code'] = session_code
        if session_name:
            data_dict['session_name'] = session_name
        if date_taken:
            data_dict['date_taken'] = date_taken

        return Session.objects.create(**data_dict)

    @staticmethod
    def manager():
        return Session.objects
