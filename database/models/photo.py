from typing import TYPE_CHECKING, Any

from django.db.models import CharField, FileField, ForeignKey, CASCADE

from database.models import Session
from database.models.base import BaseModel
from helpers.utils import generate_oid


def upload_photo(instance: "Photo", filename: str):
    _, extension = filename.split(".")
    folder_name = instance.session.oid
    return f"photos/{folder_name}/{generate_oid(7)}.{extension}"


class Photo(BaseModel):
    file = FileField(upload_to=upload_photo)
    filename = CharField(max_length=50, null=True)
    session = ForeignKey(Session, related_name="photo", on_delete=CASCADE, db_index=True)

    class Meta:
        db_table = "photo"

    def __str__(self):
        return self.file.name

    if TYPE_CHECKING:
        from django.db.models.fields.files import FieldFile
        file: FieldFile | Any
        session: Session | Any
