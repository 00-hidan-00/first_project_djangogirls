import logging
from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.forms import BaseForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

from apps.blog.models import Post

logger = logging.getLogger(__name__)


class PostRemoveView(LoginRequiredMixin, DeleteView):
    """
    Delete a blog post.
    Only the author or a superuser may do this.
    """

    model = Post
    context_object_name = "post"
    success_url = reverse_lazy("blog:post_list")

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Restrict access to author or superuser. Redirect if unauthorized."""
        try:
            self.object = self.get_object()
        except Post.DoesNotExist:
            messages.error(request, "❌ This post does not exist.")
            logger.warning(f"User {request.user.username} tried to delete a non-existing post {kwargs.get('pk')}")
            return redirect("blog:post_list")

        if not self._has_delete_permission(request.user):
            messages.error(request, "❌ You are not allowed to delete this post.")
            return redirect("blog:post_detail", pk=self.object.pk)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: BaseForm) -> HttpResponse:
        post_title = self.object.title or "Untitled"
        messages.success(self.request, f'🗑️ Post deleted: "{post_title}"')
        logger.info(f'Post "{post_title}" (ID {self.object.pk}) deleted by user {self.request.user.username}')
        return super().form_valid(form)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Disallow GET requests for delete."""
        messages.error(request, "❌ Invalid access method.")
        return redirect("blog:post_detail", pk=self.object.pk)

    def _has_delete_permission(self, user: User) -> bool:
        """Return True if user can delete this post."""
        return user == self.object.author or user.is_superuser
