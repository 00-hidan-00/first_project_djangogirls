from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

from apps.blog.models import Post


class PostRemoveView(LoginRequiredMixin, DeleteView):
    """
    View to delete a blog post and notify user upon success.
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'post'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = self.get_object()
        post_title = post.title or "Untitled"
        self._add_message(f'Post deleted: "{post_title}"')
        return super().form_valid(form)

    def _add_message(self, message: str) -> None:
        """Add a success message to be displayed to the user."""
        messages.success(self.request, message)
