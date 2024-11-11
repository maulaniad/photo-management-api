from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import CharField, EmailField, FileField, OneToOneField, CASCADE

from database.models.base import BaseModel


class Profile(BaseModel):
    name = CharField(max_length=50, blank=True, db_index=True)
    phone = CharField(max_length=15, blank=True)
    address = CharField(max_length=255, blank=True)
    avatar = FileField(upload_to="avatar/", blank=True)

    class Meta(BaseModel.Meta):
        db_table = "auth_user_profile"

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = EmailField(max_length=50, unique=True)
    profile = OneToOneField(Profile, on_delete=CASCADE, null=True)

    USERNAME_FIELD = "email"

    class Meta:
        db_table = "auth_user"

    def __str__(self):
        return self.email
