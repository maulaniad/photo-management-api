from typing import Any, Iterable

from django.core.files.uploadedfile import UploadedFile
from django.db.models import QuerySet

from api.photo.serializers import PhotoDataSerializer
from database.models import Photo
from database.repositories import PhotoRepo


class PhotoService:
    @staticmethod
    def get_photos(session_id: int | str, lazy: bool = False) -> tuple[QuerySet[Photo, Photo] | Any, str | None]:
        photos = PhotoRepo.get_photos(session_id)

        if lazy:
            return photos, None

        serializer = PhotoDataSerializer(photos, many=True)
        return serializer.data, None

    @staticmethod
    def create_photos(session_id: int | str, files: Iterable[UploadedFile]) -> tuple[Any, str | None]:
        photos = PhotoRepo.create_photos(session_id, files)
        if not photos:
            return None, "Failed to create/upload photos."

        serializer = PhotoDataSerializer(photos, many=True)
        return serializer.data, None
