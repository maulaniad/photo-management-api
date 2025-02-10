from typing import TYPE_CHECKING, Any, Self, TypeVar

from django.db.models import (Manager,
                              Model,
                              QuerySet,
                              BigAutoField,
                              CharField,
                              DateTimeField)
from django.utils import timezone

from helpers.utils import generate_oid


_TT = TypeVar('_TT', bound='BaseModel')

class CustomQuerySet(QuerySet[_TT]):
    def delete(self) -> int:
        """Soft deletes data safely by marking the deleted date on the objects."""
        return self.update(date_deleted=timezone.now())

    def hard_delete(self) -> tuple[int, dict[str, int]]:
        """Wipes data from the database."""
        return super().delete()

    def restore(self) -> int:
        """Undo soft deletions, nullifying the deleted date on the objects."""
        return self.update(date_deleted=None)

    def all(self) -> "CustomQuerySet[_TT]":
        """Fetch all objects from the database."""
        return self.filter(date_deleted__isnull=True)

    def all_with_deleted(self) -> "CustomQuerySet[_TT]":
        """Fetch all objects from the database including the soft-deleted ones."""
        return self

    def deleted_only(self) -> "CustomQuerySet[_TT]":
        """Fetch only soft-deleted objects from the database."""
        return self.filter(date_deleted__isnull=False)


class CustomManager(Manager[_TT]):
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

    def get_queryset(self) -> CustomQuerySet[_TT]:
        return CustomQuerySet(self.model, using=self._db)

    def filter(self, *args: Any, **kwargs: Any) -> CustomQuerySet[_TT]:
        return self.get_queryset().filter(*args, **kwargs)

    def all(self) -> CustomQuerySet[_TT]:
        return self.get_queryset().filter(date_deleted__isnull=True)

    def all_with_deleted(self) -> CustomQuerySet[_TT]:
        """Fetch all objects from the database including soft-deleted ones."""
        return self.get_queryset()

    def deleted_only(self) -> CustomQuerySet[_TT]:
        """Fetch only soft-deleted objects from the database."""
        return self.get_queryset().filter(date_deleted__isnull=False)


class BaseModel(Model):
    id = BigAutoField(primary_key=True, db_index=True)
    oid = CharField(max_length=21, default=generate_oid)
    date_created = DateTimeField(auto_now_add=True)
    date_updated = DateTimeField(auto_now=True)
    date_deleted = DateTimeField(null=True)

    objects: CustomManager[Self] = CustomManager()

    class Meta:
        abstract = True

    if TYPE_CHECKING:
        id: int | Any
        oid: str | Any
        date_created: DateTimeField | Any
        date_updated: DateTimeField | Any
        date_deleted: DateTimeField | Any

    def _get_all_related_objects(self):
        """Get all related objects of this model instance, handling forward and reverse relations."""
        for rel in self._meta.get_fields():
            if rel.is_relation and rel.auto_created and not rel.concrete:
                related_name = rel.get_accessor_name()                     # type: ignore
                related_manager = getattr(self, related_name)              # type: ignore

                if hasattr(related_manager, "all"):
                    yield from related_manager.all()
                else:
                    yield related_manager

    def delete(self, using: str = "default"):
        """Safe deletion through a soft-delete, marked with a deleted date. Works with CASCADE deletions."""
        self.deleted_at = timezone.now()
        self.save(using=using)

        for related_object in self._get_all_related_objects():
            if isinstance(related_object, BaseModel):
                related_object.delete(using=using)
        return self

    def hard_delete(self, using: str = "default", keep_parents: bool = False):
        """The real deletion, wiping the data from database."""
        super().delete(using=using, keep_parents=keep_parents)

    def restore(self, using: str = "default"):
        """Undo a soft-delete, nullifying the deleted date."""
        self.date_deleted = None
        self.save(using=using)
