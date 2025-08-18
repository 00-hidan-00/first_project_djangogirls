import logging
from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.edit import FormView

from apps.blog.forms import CommentForm
from apps.blog.models import Post

logger = logging.getLogger(__name__)


class AddCommentToPostView(LoginRequiredMixin, FormView):
    """
    View to add a comment to a blog post.
    Requires user to be logged in.
    """

    form_class = CommentForm
    template_name = "blog/comment/add_comment_to_post.html"

    object: Post

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Get the Post instance by pk from URL kwargs and store it for later use."""
        post_pk = kwargs.get("pk")
        if post_pk is None:
            return redirect("blog:post_list")

        self.object = get_object_or_404(Post, pk=post_pk)
        if not self.object.is_published:
            messages.error(self.request, "❌ You can't comment on an unpublished post.")
            return redirect("blog:post_list")

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form: CommentForm) -> HttpResponseRedirect:
        """Save the comment related to the blog post and redirect to post detail."""
        comment = form.save(commit=False)
        comment.post = self.object
        comment.author = self.request.user

        try:
            comment.save()
        except Exception as e:
            logger.exception(f"Error saving comment for post {self.object.pk}: {e}")
            messages.error(self.request, "❌ Error saving your comment. Please try again later.")
            return redirect("blog:post_detail", pk=self.object.pk)

        comment_text = comment.text[:20] + "…" if len(comment.text) > 20 else comment.text
        messages.success(self.request, f'💬 Comment added: "{comment_text}"')
        logger.info(
            f"Comment added by user {self.request.user.username} (ID: {self.request.user.pk}) "
            f'to post "{self.object.title}" (ID: {self.object.pk}): "{comment_text}"'
        )

        return super().form_valid(form)
