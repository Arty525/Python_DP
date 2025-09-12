from django.core.management.base import BaseCommand
from django.core.management import call_command
from restaurant.models import Table


class Command(BaseCommand):
    help = "Adds tables to database"

    def handle(self, *args, **options):
        Table.objects.all().delete()
        call_command("loaddata", "fixtures/tables_fixture.json")
        self.stdout.write(self.style.SUCCESS("Successfully added tables"))