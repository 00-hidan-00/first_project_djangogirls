from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import FormView

from apps.blog.forms import CommentForm
from apps.blog.models import Post


class AddCommentToPostView(LoginRequiredMixin, FormView):
    """
    View to add a comment to a blog post.
    Requires user to be logged in.
    """

    form_class = CommentForm
    template_name = "blog/add_comment_to_post.html"

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Get the Post instance by pk from URL kwargs and store it for later use."""
        self.blog_post = get_object_or_404(Post, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Save the comment related to the blog post and redirect to post detail."""
        comment = form.save(commit=False)
        comment.post = self.blog_post
        comment.save()
        messages.info(self.request, f'Comment created: "{comment.text}"')
        return redirect("blog:post_detail", pk=self.blog_post.pk)
