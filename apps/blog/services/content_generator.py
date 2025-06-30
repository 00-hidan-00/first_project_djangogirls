import logging
import random
from datetime import datetime
from typing import Iterator
from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from faker import Faker

from apps.blog.models import Comment
from apps.blog.models import Post

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ContentGenerator:
    def __init__(self):
        self.fake = Faker()
        self.tz = timezone.get_current_timezone()
        self.User = get_user_model()
        self._posts_cache = list(Post.objects.all())
        self._users_cache = list(self.User.objects.all())

        if not self._users_cache:
            raise ValueError("No users found in the database.")
        if not self._posts_cache:
            logger.warning("No posts found — comment generation will be skipped.")

    def _random_user(self) -> AbstractBaseUser:
        return random.choice(self._users_cache)

    def _random_title(self, max_words: int = 10) -> str:
        return self.fake.sentence(nb_words=max_words).rstrip('.')

    def _random_text(self, max_chars: int = 200) -> str:
        return self.fake.text(max_nb_chars=max_chars)

    def _random_created_date(self, date: datetime = '-30d') -> datetime:
        naive_date = self.fake.date_time_between(start_date=date, end_date='now')
        created_date = timezone.make_aware(naive_date, timezone=self.tz)
        return created_date

    def _maybe_published_date(self, date: datetime) -> Optional[datetime]:
        if random.choice([True, False]):
            naive_published_date = self.fake.date_time_between(start_date=date, end_date='now')
            published_date = timezone.make_aware(naive_published_date, timezone=self.tz)
        else:
            published_date = None
        return published_date

    @staticmethod
    def _next_local_number(post: Post, offset: int) -> int:
        last_comment = post.comments.order_by('-local_number').first()
        base = last_comment.local_number if last_comment else 0
        return base + offset + 1

    def refresh_posts_cache(self):
        self._posts_cache = list(Post.objects.all())

    def generate_posts(self, amount: int) -> Iterator[Post]:
        posts = []
        for _ in range(amount):
            created = self._random_created_date()
            post = Post(
                author=self._random_user(),
                title=self._random_title(),
                text=self._random_text(),
                created_date=created,
                published_date=self._maybe_published_date(created),
            )
            posts.append(post)
        return posts

    def generate_comments(self, max_per_post: int) -> Iterator[Comment]:
        comments_list = []
        if not self._posts_cache:
            return comments_list

        for post in self._posts_cache:
            comment_count = random.randint(1, max_per_post)
            for i in range(comment_count):
                comments_list.append(
                    Comment(
                        post=Post.objects.get(pk=post.pk),
                        author=self._random_user(),
                        text=self._random_text(),
                        local_number=self._next_local_number(post=post, offset=i),
                        approved_comment=random.choice([True, False])
                    )
                )

        return comments_list
