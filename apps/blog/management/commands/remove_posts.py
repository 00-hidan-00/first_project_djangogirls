import logging

from django.core.management.base import BaseCommand, CommandParser

from apps.blog.models import Post

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = 'Delete all posts from the blog.'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Delete without confirmation prompt.'
        )

    def handle(self, *args, **options):
        force = options['force']

        if not force:
            confirm = input("Are you sure you want to delete ALL posts? Type 'yes' to confirm: ")
            if confirm.strip().lower() not in ('yes', 'y'):
                logger.warning("Aborted. No posts deleted.")
                return

        deleted_count, _ = Post.objects.all().delete()
        logger.info(f"Deleted {deleted_count} posts.")
