import logging

from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction

from apps.blog.models import Comment, Post
from apps.blog.services import ContentGenerator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = 'Generate Post and Comment'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '--amount_posts',
            type=int,
            default=10,
            help='Number of posts to generate (default: 10)'
        )
        parser.add_argument(
            '--amount_comments',
            type=int,
            default=5,
            help='Number of comments to generate for each post (default: 5)'
        )

    def handle(self, *args, **options) -> None:
        amount_posts = options['amount_posts']
        amount_comments = options['amount_comments']
        generator = ContentGenerator()
        logger.info(
            f"Starting post and comment generation."
            f"\nExisting Post: {Post.objects.count()}"
            f"\nExisting Comment: {Comment.objects.count()}"
        )
        try:
            with transaction.atomic():
                posts = generator.generate_posts(amount_posts)
                Post.objects.bulk_create(posts)
                generator.refresh_posts_cache()
                comments = generator.generate_comments(amount_comments)
                Comment.objects.bulk_create(comments)
            logger.info(f"Created {len(posts)} posts:\n" + "\n".join(f" • {post.title}" for post in posts))
            logger.info(
                f"Created {len(comments)} comments:\n" +
                "\n".join(f" • {comment.text[:40]}" for comment in comments[:5]) +
                ("\n • ..." if len(comments) > 5 else "")
            )
            logger.info(
                f"Total post after generation: {Post.objects.count()}. Total comment after generation: {Comment.objects.count()}"
            )
        except ValueError as e:
            logger.error(f"Error: {e}")
