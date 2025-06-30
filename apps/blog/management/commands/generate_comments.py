import logging

from django.core.management.base import BaseCommand, CommandParser

from apps.blog.management.commands.generate_posts import ContentGenerator
from apps.blog.models import Comment

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = 'Generate dummy comments for posts.'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '--amount',
            type=int,
            default=5,
            help='Number of comments to generate for each post (default: 5)'
        )

    def handle(self, *args, **options) -> None:
        amount = options['amount']
        generator = ContentGenerator()
        logger.info(f"Starting comment generation. Existing comments: {Comment.objects.count()}")
        try:
            comments = generator.generate_comments(amount)
            if not comments:
                logger.warning("No comments generated (possibly no posts or users).")
                return
            Comment.objects.bulk_create(comments)
            logger.info(
                f"Created {len(comments)} comments:\n" + "\n".join(
                    f" • {comment.text[:40]}" for comment in comments[:5]
                )
            )
            logger.info(f"Total comments after generation: {Comment.objects.count()}")
        except ValueError as e:
            logger.error(f"Generation failed: {e}")
