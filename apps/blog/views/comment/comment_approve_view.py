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
from apps.blog.utils import log_comment_action

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

        self.object = get_object_or_404(
            Comment.objects.select_related("post"), post__pk=kwargs.get("pk"), local_number=kwargs.get("local_number")
        )

        if not self.object.can_be_modified_by(request.user):
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

        log_comment_action(request, self.object, "approved")

        return redirect("blog:post_detail", pk=self.object.post.pk)
