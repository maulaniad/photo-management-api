from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import EmailField, OneToOneField, CASCADE

from database.models import Profile
from database.models.base import BaseModel


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = EmailField(max_length=50, unique=True)
    profile = OneToOneField(Profile, on_delete=CASCADE, null=True, related_name="user")

    USERNAME_FIELD = "email"

    class Meta:
        db_table = "auth_user"

    def __str__(self):
        return self.email
