from django.db.models import CharField, FileField, TextField

from database.models.base import BaseModel


def upload_avatar(instance: "Profile", filename: str):
    folder_name = instance.oid
    extension = filename.split(".")[-1]
    new_filename = f"avatar.{extension}"
    return f"avatars/{folder_name}/{new_filename}"


class Profile(BaseModel):
    name = CharField(max_length=50, null=True, db_index=True)
    bio = TextField(max_length=1000, null=True)
    address = CharField(max_length=255, null=True)
    avatar = FileField(upload_to=upload_avatar, null=True)

    class Meta(BaseModel.Meta):
        db_table = "auth_user_profile"

    def __str__(self):
        return self.name
