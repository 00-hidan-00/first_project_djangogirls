from django.db.models.query import QuerySet
from django.utils import timezone
from django.views.generic import ListView

from apps.blog.models import Post


class PostListView(ListView):
    """
    Display all published blog posts.
    Visible to any user.
    """

    model = Post
    template_name = "blog/post/post_list.html"
    context_object_name = "posts"

    def get_queryset(self) -> QuerySet[Post]:
        """Return published posts ordered by newest first."""
        return self.model.objects.filter(published_date__lte=timezone.now()).order_by("-published_date")
