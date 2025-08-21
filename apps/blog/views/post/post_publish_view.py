import logging
from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import DatabaseError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST

from apps.blog.models import Post

logger = logging.getLogger(__name__)


@method_decorator(require_POST, name="dispatch")
class PostPublishView(LoginRequiredMixin, View):
    """
    Publish a blog post.
    Only the author or a superuser may do this.
    """

    object: Post
    post_pk: int

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Restrict access to author or superuser. Redirect if unauthorized."""
        self.object = get_object_or_404(Post, pk=kwargs.get("pk"))
        self.post_pk = self.object.pk
        if not self.object.is_visible_to(request.user):
            logger.warning(f"User {request.user.id} tried to publish post {self.post_pk} without permission.")
            messages.error(request, "❌ You are not allowed to publish this post.")
            return redirect("blog:post_list")

        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Publish the post, log and notify, then redirect."""

        try:
            self.object.publish()
        except DatabaseError as e:
            logger.exception(f"Error publishing post {self.post_pk}: {e}")
            messages.error(request, "❌ An error occurred while publishing the post. Please try again later.")
            return redirect("blog:post_detail", pk=self.post_pk)
        except Exception as e:
            logger.exception(f"Unexpected error while publishing post {self.post_pk}: {e}")
            messages.error(request, "❌ An unexpected error occurred. Please try again later.")
            return redirect("blog:post_detail", pk=self.post_pk)

        logger.info(f'Post "{self.object.title}" (ID {self.post_pk}) published by user {request.user.username}')
        messages.success(request, f'🎉 Post published: "{self.object.title}"')

        return redirect("blog:post_detail", pk=self.post_pk)
