import logging
import random
from datetime import datetime
from typing import Iterator
from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.core.management.base import BaseCommand, CommandParser
from django.utils import timezone
from faker import Faker

from apps.blog.models import Post

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PostGenerator:
    def __init__(self):
        self.fake = Faker()
        self.tz = timezone.get_current_timezone()
        self.User = get_user_model()

    def _get_random_user(self) -> AbstractBaseUser:
        users = list(self.User.objects.all())
        if not users:
            raise ValueError("No users found in database")
        return random.choice(users)

    def _random_title(self, max_words: int = 10) -> str:
        return self.fake.sentence(nb_words=max_words).rstrip('.')

    def _random_text(self, max_chars: int = 200) -> str:
        return self.fake.text(max_nb_chars=max_chars)

    def _random_created_date(self) -> datetime:
        naive_date = self.fake.date_time_between(start_date='-30d', end_date='now')
        created_date = timezone.make_aware(naive_date, timezone=self.tz)
        return created_date

    def _maybe_published_date(self, date: datetime) -> Optional[datetime]:
        if random.choice([True, False]):
            naive_published_date = self.fake.date_time_between(start_date=date, end_date='now')
            published_date = timezone.make_aware(naive_published_date, timezone=self.tz)
        else:
            published_date = None
        return published_date

    def generate_posts(self, amount: int) -> Iterator[Post]:
        return [
            Post(
                author=self._get_random_user(),
                title=self._random_title(),
                text=self._random_text(),
                created_date=(created := self._random_created_date()),
                published_date=self._maybe_published_date(created)
            )
            for _ in range(amount)
        ]


class Command(BaseCommand):
    help = 'Generate dummy blog posts.'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            '--amount',
            type=int,
            default=10,
            help='Number of posts to generate (default: 10)'
        )

    def handle(self, *args, **options):
        amount = options['amount']
        generator = PostGenerator()

        logger.info(f"Starting post generation. Existing posts: {Post.objects.count()}")

        try:
            posts = generator.generate_posts(amount)
            Post.objects.bulk_create(posts)

            logger.info("Posts created successfully:")

            for post in posts:
                logger.info(f" • {post.title}")

            logger.info(f"Total posts after generation: {Post.objects.count()}")

        except ValueError as e:
            logger.error(f"Error: {e}")
