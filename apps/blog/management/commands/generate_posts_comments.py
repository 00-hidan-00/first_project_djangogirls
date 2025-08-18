import logging

from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction

from apps.blog.models import Comment, Post
from apps.blog.services import ContentGenerator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = "Generate Post and Comment"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--amount_posts", type=int, default=10, help="Number of posts to generate (default: 10)")
        parser.add_argument(
            "--amount_comments", type=int, default=5, help="Number of comments to generate for each post (default: 5)"
        )

    def handle(self, *args, **options) -> None:
        amount_posts = options["amount_posts"]
        amount_comments = options["amount_comments"]
        generator = ContentGenerator()
        logger.info(
            "Starting post and comment generation.\nExisting Post: %d\nExisting Comment: %d",
            Post.objects.count(),
            Comment.objects.count(),
        )
        try:
            with transaction.atomic():
                posts = generator.generate_posts(amount_posts)
                Post.objects.bulk_create(posts)
                generator.refresh_posts_cache()
                comments = generator.generate_comments(amount_comments)
                Comment.objects.bulk_create(comments)
            logger.info("Created %d posts: \n%s", len(posts), "\n".join(f" • {post.title}" for post in posts))
            logger.info(
                "Created %d comments: \n%s%s",
                len(comments),
                "\n".join(f" • {comment.text.replace('\n', ' ')[:40]} ..." for comment in comments[:5]),
                "\n • ..." if len(comments) > 5 else "",
            )
            logger.info(
                "Total post after generation: %d. Total comment after generation: %d",
                Post.objects.count(),
                Comment.objects.count(),
            )
        except ValueError as e:
            logger.error("Error: %s", e)
