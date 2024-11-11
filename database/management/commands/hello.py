from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    help = "Prints 'Hello, World!'"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("name", nargs="*")

    def handle(self, *args, **options):
        name = options.get('name', None)
        if not name or name == "":
            self.stdout.write(self.style.SUCCESS("Hello, World!"))
            return

        self.stdout.write(self.style.WARNING(f"Hello, {", ".join(name)}!"))
