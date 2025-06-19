from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from apps.blog.models import Post


class PostDraftListView(LoginRequiredMixin, ListView):
    """
    View to display a list of draft posts (posts without a published date).
    Only authenticated users can access this view.
    """
    model = Post
    template_name = 'blog/post_draft_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """
        Returns all posts that are not yet published (drafts),
        ordered by creation date in ascending order.
        """

        return self.model.objects.filter(published_date__isnull=True).order_by('created_date')
