from django.core.management.base import BaseCommand, CommandParser
from django.db.transaction import atomic

from database.models.profile import Profile
from database.models.user import User


class Command(BaseCommand):
    help = "Create a new profile following the User ID"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("user_id", nargs="*")

    @atomic
    def handle(self, *args, **options):
        user_id = options.get('user_id', None)

        if not user_id:
            self.stdout.write(self.style.WARNING("User ID Cannot be Empty!"))
            return

        user_id = int(user_id[0])
        user_object = User.objects.filter(id=user_id).first()

        if not user_object:
            self.stdout.write(self.style.WARNING("User ID Not Found!"))
            return

        name = input("Enter Name: ")

        new_profile = Profile.objects.create(name=name)
        user_object.profile = new_profile
        user_object.save()

        self.stdout.write(self.style.SUCCESS("Success Created a new Profile"))
