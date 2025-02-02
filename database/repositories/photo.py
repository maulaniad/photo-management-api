from typing import Iterable

from django.core.files.uploadedfile import UploadedFile
from django.db.models import Q

from database.models import Photo
from database.repositories import SessionRepo


class PhotoRepo:
    @staticmethod
    def get_photos(session_id: int | str):
        return Photo.objects.filter(
            Q(session__id=session_id) if isinstance(session_id, int)
            else Q(session__oid=session_id)
        ).all()

    @staticmethod
    def get_photo(photo_id: int | str):
        return Photo.objects.filter(
            Q(id=photo_id) if isinstance(photo_id, int) else Q(oid=photo_id)
        ).first()

    @staticmethod
    def create_photos(session_id: int | str, files: Iterable[UploadedFile]):
        session = SessionRepo.get_session_by_id(session_id)
        if not session:
            return None

        photo_instances = []

        for file in files:
            filename, extension = "VBLANK_DEFAULT", ".jpg"

            if file and file.name:
                filename, extension = file.name.rsplit(".", 1)

                if len(filename) > 50 - len(extension) - 1:
                    filename = filename[:50 - len(extension) - 1]

            photo_instances.append(
                Photo(file=file, session=session, filename=f"{filename}.{extension}")
            )

        photos = Photo.objects.bulk_create(photo_instances, batch_size=50)
        return photos

    @staticmethod
    def delete_photos(photo_ids: Iterable[int | str]):
        photos = Photo.objects.filter(
            Q(id__in=[pid for pid in photo_ids if isinstance(pid, int)]) |
            Q(oid__in=[pid for pid in photo_ids if isinstance(pid, str)])
        )

        photos.delete()
        return True
