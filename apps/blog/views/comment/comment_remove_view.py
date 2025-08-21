import logging
from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.forms import BaseForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

from apps.blog.models import Comment
from apps.blog.utils import log_comment_action

logger = logging.getLogger(__name__)


class CommentRemoveView(LoginRequiredMixin, DeleteView):
    """
    Delete a comment and redirect to its associated post detail view.
    Only the comment's author or a superuser can delete the comment.
    Displays a warning message after successful deletion.
    Requires authenticated user (via LoginRequiredMixin).
    """

    model = Comment
    context_object_name = "comment"

    def get_object(self, queryset: QuerySet[Comment] | None = None) -> Comment:
        """
        Get Comment by post PK and local_number instead of default PK.
        Supports nested URL lookup and improves URL clarity.
        """
        return get_object_or_404(
            Comment.objects.select_related("post"),
            post__pk=self.kwargs.get("pk"),
            local_number=self.kwargs.get("local_number"),
        )

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Check permissions before any action:
        only comment's author or a superuser can delete.
        Otherwise, redirect to post detail with error.
        """
        self.object = self.get_object()

        if not self.object.can_be_modified_by(request.user):
            messages.error(request, "❌ You are not allowed to delete this comment.")
            return redirect("blog:post_detail", pk=self.object.post.pk)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Disallow GET requests for delete."""
        messages.error(request, "❌ Invalid access method.")
        return redirect("blog:post_detail", pk=self.object.post.pk)

    def form_valid(self, form: BaseForm) -> HttpResponse:
        """Attempt to delete the comment, handle success and errors,add feedback messages and logging."""
        try:
            response = super().form_valid(form)
        except Exception as e:
            logger.exception(f"Error deleting comment {getattr(self.object, 'pk', 'N/A')}: {e}")
            messages.error(self.request, "❌ Error deleting comment. Please try again later.")
            return redirect("blog:post_detail", pk=self.object.post.pk)

        log_comment_action(self.request, self.object, "deleted")

        return response

    def get_success_url(self) -> str:
        """Redirect to the related post detail page after successful deletion."""
        return reverse_lazy("blog:post_detail", kwargs={"pk": self.object.post.pk})
