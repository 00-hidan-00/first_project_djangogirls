import logging

from django.core.management.base import BaseCommand, CommandParser

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = 'Generate Post and Comment'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('amount', type=int, )

    def handle(self, *args, **options):
        ...
