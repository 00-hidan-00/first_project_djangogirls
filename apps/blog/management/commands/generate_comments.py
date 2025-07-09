import logging

from django.core.management.base import BaseCommand, CommandParser

from apps.blog.models import Comment
from apps.blog.services import ContentGenerator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = "Generate dummy comments for posts."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--amount", type=int, default=5, help="Number of comments to generate for each post (default: 5)"
        )

    def handle(self, *args, **options) -> None:
        amount = options["amount"]
        generator = ContentGenerator()
        logger.info("Starting comment generation. Existing comments: %d", Comment.objects.count())
        try:
            comments = generator.generate_comments(amount)
            if not comments:
                logger.warning("No comments generated (possibly no posts or users).")
                return
            Comment.objects.bulk_create(comments)
            logger.info(
                "Created %d comments: \n%s",
                len(comments),
                "\n".join(f" • {comment.text.replace('\n', ' ')[:40]} ..." for comment in comments[:5]),
            )

            logger.info("Total comments after generation: %d", Comment.objects.count())
        except ValueError as e:
            logger.error("Generation failed: %s", e)
