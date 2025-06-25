from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    help = 'Generate Comment'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('amount', type=int, )

    def handle(self, *args, **options):
        ...
