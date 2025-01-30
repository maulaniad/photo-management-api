from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    help = "Prints welcome message."

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("name", nargs="*")

    def handle(self, *args, **options):
        name = options.get('name', None)
        if not name or name == "":
            self.stdout.write(
                self.style.SUCCESS("Hello ") +
                self.style.WARNING("Python ") +
                self.style.SUCCESS("from Django commands!")
            )
            return

        self.stdout.write(
            self.style.SUCCESS(f"Hello, {", ".join(name)}!"),
        )
