from decouple import config

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from database.repositories.user import UserRepo
from database.repositories.profile import ProfileRepo


class Command(BaseCommand):
    help = "Seeds the database with necessary data (including admin user)."

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO("Seed: Getting from environment ..."))
        admin_email = config('SEED_ADMIN_EMAIL', cast=str, default="")
        admin_phone = config('SEED_ADMIN_PHONE', default=None)
        admin_password = config('SEED_ADMIN_PASSWORD', cast=str, default="")

        self.stdout.write(self.style.HTTP_INFO("Seed: Creating Admin user ..."))
        try:
            admin = UserRepo.create_user(
                email=admin_email,                          # type: ignore
                phone=admin_phone,                          # type: ignore
                password=make_password(admin_password),     # type: ignore
                is_superuser=True
            )
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f"Seed: {e}"))
            return

        self.stdout.write(self.style.HTTP_INFO("Seed: Updating Admin profile ..."))
        admin.profile = ProfileRepo.update_or_create_profile(
            admin.pk,
            name="Admin",
            bio="Admin",
            address="Admin"
        )
        admin.save()

        self.stdout.write(self.style.SUCCESS("Seed: Admin user created."))
