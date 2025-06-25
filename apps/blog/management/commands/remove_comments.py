import logging

from django.core.management.base import BaseCommand, CommandParser

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = 'Delete all comments from the blog.'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument()

    def handle(self, *args, **options):
        ...
