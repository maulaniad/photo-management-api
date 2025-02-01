from rest_framework.serializers import ModelSerializer, IntegerField

from database.models import Session


class ValidateCreateSession(ModelSerializer):
    class Meta:
        model = Session
        fields = ["date_taken", "session_code", "session_name"]


class SessionDataSerializer(ModelSerializer):
    total_photos = IntegerField(read_only=True, default=0)

    class Meta:
        model = Session
        fields = [
            "oid",
            "date_created",
            "date_updated",
            "date_deleted",
            "date_taken",
            "session_code",
            "session_name",
            "total_photos"
        ]
