from random import choice
from string import ascii_uppercase, digits
from typing import TYPE_CHECKING, Any

from django.db.models import CharField, DateTimeField
from django.utils.timezone import now

from database.models.base import BaseModel
from helpers.utils import generate_oid


def create_session_code():
    random_letters = "".join(choice(ascii_uppercase) for _ in range(4))
    random_digits = "".join(choice(digits) for _ in range(4))
    return f"{random_letters}-{random_digits}"


def create_session_name():
    return f"Photo Session {generate_oid(length=6)}"


class Session(BaseModel):
    date_taken = DateTimeField(default=now)
    session_code = CharField(max_length=25, default=create_session_code, db_index=True)
    session_name = CharField(max_length=50, default=create_session_name)

    class Meta:
        db_table = "session"

    def __str__(self):
        return self.session_code

    if TYPE_CHECKING:
        from datetime import datetime
        date_taken: datetime | Any
        session_code: str | Any
