import logging

from django.core.management.base import BaseCommand, CommandParser

from apps.blog.models import Post
from apps.blog.services import ContentGenerator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = "Generate dummy blog posts."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--amount", type=int, default=10, help="Number of posts to generate (default: 10)")

    def handle(self, *args, **options) -> None:
        amount = options["amount"]
        generator = ContentGenerator()
        logger.info("Starting post generation. Existing posts: %d", Post.objects.count())
        try:
            posts = generator.generate_posts(amount)
            Post.objects.bulk_create(posts)
            logger.info("Created %d posts: \n%s", len(posts), "\n".join(f" • {post.title}" for post in posts))
            logger.info("Total posts after generation: %d", Post.objects.count())
        except ValueError as e:
            logger.error("Generation failed: %s", e)
