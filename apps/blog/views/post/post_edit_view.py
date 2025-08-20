import logging
from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import UpdateView

from apps.blog.forms import PostForm
from apps.blog.mixins import PostBaseEditMixin
from apps.blog.models import Post

logger = logging.getLogger(__name__)


class PostEditView(LoginRequiredMixin, PostBaseEditMixin, UpdateView):
    """
    Edit an existing blog post.
    Only the author or a superuser may do this.
    """

    model = Post
    form_class = PostForm
    template_name = "blog/post/post_edit.html"
    context_object_name = "post"
    is_edit = True

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Restrict access to author or superuser. Redirect if unauthorized."""
        try:
            self.object = self.get_object()
        except Post.DoesNotExist:
            messages.error(request, "❌ This post does not exist.")
            logger.error(f"User {request.user.username} tried to edit a non-existing post {kwargs.get('pk')}")
            return redirect("blog:post_list")
        user = request.user

        if not self.object.is_visible_to(user):
            messages.error(request, "❌ You are not allowed to edit this post.")
            logger.warning(f"User {user.username} tried to edit post {self.object.pk} without permission.")
            return redirect("blog:post_detail", pk=self.object.pk)

        return super().dispatch(request, *args, **kwargs)

    def _get_success_message(self, post_object: Post, is_publish: bool) -> str:
        """Return success message for save."""
        if is_publish:
            message = f'🎉 Post updated and published: "{post_object.title}"'
            logger.info(
                f'Post "{post_object.title}" (ID {post_object.pk}) published by user {post_object.author.username}'
            )
        else:
            message = f'💾 Post updated and saved as draft: "{post_object.title}"'
            logger.info(
                f'Post "{post_object.title}" (ID {post_object.pk}) saved as draft by user {post_object.author.username}'
            )
        return message
