from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

from apps.blog.models import Comment


class CommentRemoveView(LoginRequiredMixin, DeleteView):
    """
    Delete a comment and redirect to its associated post detail view.
    Displays a warning message after successful deletion.
    Requires authenticated user.
    """
    model = Comment
    context_object_name = 'comment'

    def get_queryset(self):
        """Optimize queryset by selecting related post."""
        return super().get_queryset().select_related('post')

    def get_success_url(self) -> str:
        """Redirect to the related post detail page after deletion."""
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})

    def form_valid(self, form) -> HttpResponse:
        """Delete comment, add message, then redirect."""
        comment_text = self.object.text or '[empty]'
        response = super().form_valid(form)
        messages.warning(self.request, f'Comment deleted: "{comment_text}"')
        return response
