from typing import Any, Generic, Iterable, Optional, Self, Sequence, TypeVar

from django.db.models import (Manager,
                              Model,
                              QuerySet,
                              BigAutoField,
                              CharField,
                              DateTimeField)
from django.utils import timezone

from helpers.utils import generate_oid


_TT = TypeVar('_TT', bound='BaseModel')

class CustomQuerySet(QuerySet, Generic[_TT]):
    def first(self) -> Optional[Self]:
        return super().first()

    def get(self, *args: Any, **kwargs: Any) -> Self:
        return super().get(*args, **kwargs)


class CustomManager(Generic[_TT], Manager[_TT]):
    def get_by_natural_key(self, username):
        """Used internally by Django. DO NOT USE THIS METHOD."""
        return self.get(**{self.model.USERNAME_FIELD: username})  # type: ignore

    def create_user(self, email, name, password=None, **extra_fields):
        """Used by Management Commands. DO NOT USE THIS METHOD."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)  # type: ignore
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)  # type: ignore
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        """Used by Management Commands. DO NOT USE THIS METHOD."""
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, name, password, **extra_fields)

    def get_queryset(self) -> QuerySet[_TT] | CustomQuerySet[_TT]:
        return super().get_queryset().filter(date_deleted__isnull=True)

    def all_with_deleted(self) -> QuerySet[_TT]:
        """Fetch all objects from the database including soft-deleted ones."""
        return super().get_queryset()

    def deleted_only(self) -> QuerySet[_TT]:
        """Fetch only soft-deleted objects from the database."""
        return super().get_queryset().filter(date_deleted__isnull=False)

    def create(self, **kwargs: Any) -> _TT:
        """Create a new object and save it to the database."""
        return super().create(**kwargs)

    def bulk_create(self, objects: Iterable[Any], batch_size: int | Any = ..., ignore_conflicts: bool | Any = ..., update_conflicts: bool | Any = ..., update_fields: Sequence[str] | Any = ..., unique_fields: Sequence[str] | Any = ...) -> list[_TT]:
        """Bulk create objects and save them to the database."""
        return super().bulk_create(objects, batch_size, ignore_conflicts, update_conflicts, update_fields, unique_fields)

    def bulk_update(self, objects: Iterable[Any], fields: Sequence[str], batch_size: int | Any = ...) -> int:
        """Bulk update objects and save them to the database."""
        return super().bulk_update(objects, fields, batch_size)

    def delete(self):
        """Soft deletes data safely by marking the deleted date on the objects."""
        return super().update(date_deleted=timezone.now())

    def hard_delete(self):
        """Wipes data from the database."""
        return super().delete()                     # type: ignore

    def restore(self):
        """Undo soft deletions, nullifying the deleted date on the objects."""
        return super().update(date_deleted=None)


class BaseModel(Model):
    id = BigAutoField(primary_key=True)
    oid = CharField(max_length=21, default=generate_oid)
    date_created = DateTimeField(auto_now_add=True)
    date_updated = DateTimeField(auto_now=True)
    date_deleted = DateTimeField(null=True)

    objects: CustomManager[Self] = CustomManager()

    class Meta:
        abstract = True

    def delete(self, using: str = "default"):
        """Safe deletion through a soft-delete, marked with a deleted date."""
        self.date_deleted = timezone.now()
        self.save(using=using)
        return self

    def hard_delete(self, using: str = "default", keep_parents: bool = False):
        """The real deletion, wiping the data from database."""
        super().delete(using=using, keep_parents=keep_parents)

    def restore(self, using: str = "default"):
        """Undo a soft-delete, nullifying the deleted date."""
        self.date_deleted = None
        self.save(using=using)
