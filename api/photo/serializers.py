from django.core.files.uploadedfile import UploadedFile
from rest_framework.serializers import (ModelSerializer,
                                        Serializer,
                                        FileField,
                                        ListField,
                                        ValidationError)

from database.models import Photo


class ValidateCreatePhotos(Serializer):
    files = ListField(
        child=FileField(),
        allow_empty=False
    )

    def validate_files(self, files: list[UploadedFile]):
        if not files:
            raise ValidationError("No files provided.")

        for file in files:
            if not file.content_type:
                continue

            if not file.content_type.startswith("image/"):
                raise ValidationError("Only image files are allowed.")

        return files


class PhotoDataSerializer(ModelSerializer):
    class Meta:
        model = Photo
        exclude = ["id", "session"]
