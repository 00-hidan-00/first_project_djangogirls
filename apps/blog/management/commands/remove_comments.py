import logging

from django.core.management.base import BaseCommand, CommandParser

from apps.blog.models import Comment

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = 'Delete all comments from the blog.'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '--force',
            action='store_true',
            help='Delete without confirmation prompt.'
        )

    def handle(self, *args, **options) -> None:
        force = options['force']
        if not force:
            confirm = input("Are you sure you want to delete ALL comments? Type 'yes' to confirm: ")
            if confirm.strip().lower() not in ('yes', 'y'):
                logger.warning("Aborted. No comments deleted.")
                return
        deleted_count, _ = Comment.objects.all().delete()
        logger.info(f"Deleted {deleted_count} comments.")
