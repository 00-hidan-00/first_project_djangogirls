from __future__ import annotations

from typing import Any

from django.conf import settings
from django.db import models
from django.db.models import Q, QuerySet
from django.utils import timezone

from apps.users.models import User


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title

    def publish(self) -> None:
        """Set published_date to now and save the post."""
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self) -> QuerySet[Comment]:
        return self.comments.filter(approved_comment=True)

    def is_visible_to(self, user) -> bool:
        """Check if the post is visible to the given user (author or superuser)."""
        return user == self.author or user.is_superuser

    def visible_comments_for(self, user: User) -> QuerySet[Comment]:
        """
        Return comments visible to the given user:
        - All comments for superusers
        - Approved + own comments for authenticated users
        - Only approved comments for anonymous users
        """
        if user.is_superuser:
            return self.comments.all()
        elif user.is_authenticated:
            return self.comments.filter(Q(approved_comment=True) | Q(author=user)).distinct()
        else:
            return self.comments.filter(approved_comment=True)

    @property
    def is_published(self) -> bool:
        return self.published_date is not None


class Comment(models.Model):
    post = models.ForeignKey("blog.Post", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    local_number = models.PositiveIntegerField("Local Number", editable=False, null=True, blank=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["post", "local_number"], name="unique_comment_number_per_post")]

    def __str__(self) -> str:
        return f"{self.author} (post_id={self.post_id}): {self.text[:50]}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Assign or recalc local_number on save."""
        if not self.pk or (Comment.objects.only("post").get(pk=self.pk).post_id != self.post_id):
            self.local_number = self._next_local_number()
        super().save(*args, **kwargs)

    def approve(self) -> None:
        """Mark comment as approved and save."""
        self.approved_comment = True
        self.save()

    def can_be_modified_by(self, user) -> bool:
        return self.author == user or user.is_superuser

    def _next_local_number(self) -> int:
        """Get next sequential local_number for the post's comments."""
        last = Comment.objects.filter(post=self.post).order_by("-local_number").first()
        return (last.local_number + 1) if last else 1
