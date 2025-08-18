import logging
from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST

from apps.blog.models import Comment

logger = logging.getLogger(__name__)


@method_decorator(require_POST, name="dispatch")
class CommentApproveView(LoginRequiredMixin, View):
    """
    View to approve a comment.
    Only the comment's author or a superuser can approve.
    Accepts only POST requests.
    """

    object: Comment

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Check user permission to approve the comment before processing the request.
        Redirect with error if unauthorized.
        """
        pk: int | None = kwargs.get("pk")
        local_number: int | None = kwargs.get("local_number")
        self.object = get_object_or_404(Comment, post__pk=pk, local_number=local_number)

        if self.object.author != request.user and not request.user.is_superuser:
            messages.error(request, "❌ You are not allowed to approve this comment.")
            return redirect("blog:post_detail", pk=self.object.post.pk)

        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Approve the comment and redirect to the post detail page."""
        try:
            self.object.approve()
        except Exception as e:
            logger.exception(f"Error approving comment {self.object.pk}: {e}")
            messages.error(request, "❌ Error approving the comment. Please try again later.")
            return redirect("blog:post_detail", pk=self.object.post.pk)

        comment_text = self.object.text[:20] + "…" if len(self.object.text) > 20 else self.object.text
        messages.success(request, f'✅ Comment approved: "{comment_text}"')
        logger.info(
            f"Comment approved by user {self.request.user.username} (ID: {self.request.user.pk}) "
            f'to post "{self.object.post.title}" (ID: {self.object.post.pk}): "{comment_text}"'
        )

        return redirect("blog:post_detail", pk=self.object.post.pk)
