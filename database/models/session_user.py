from typing import TYPE_CHECKING, Any

from django.db.models import ForeignKey, CASCADE

from database.models import User, Session
from database.models.base import BaseModel


class SessionUser(BaseModel):
    user = ForeignKey(User, related_name="user", on_delete=CASCADE, db_index=True)
    session = ForeignKey(Session, related_name="session", on_delete=CASCADE, db_index=True)

    class Meta:
        db_table = "session_users"

    if TYPE_CHECKING:
        user: User | Any
        session: Session | Any
