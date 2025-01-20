from django.db.models import CharField, FileField

from database.models.base import BaseModel


class Profile(BaseModel):
    name = CharField(max_length=50, null=True, db_index=True)
    phone = CharField(max_length=15, null=True)
    address = CharField(max_length=255, null=True)
    avatar = FileField(upload_to="avatar/", null=True)

    class Meta(BaseModel.Meta):
        db_table = "auth_user_profile"

    def __str__(self):
        return self.name
