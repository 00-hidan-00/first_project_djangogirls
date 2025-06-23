from django.utils import timezone
from django.views.generic import ListView

from apps.blog.models import Post


class PostListView(ListView):
    """
    Display a list of published Post objects ordered by most recent published date.
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return self.model.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
