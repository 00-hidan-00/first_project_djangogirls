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
        queryset = self.model.objects.filter(published_date__lte=timezone.now()).order_by("-published_date")

        if self.request.user.is_authenticated:
            favorite_ids = set(self.request.user.favorites.values_list("id", flat=True))
        else:
            favorite_ids = set(self.request.session.get("post_favorites", []))

        for post in queryset:
            post.is_favorited = post.id in favorite_ids

        return queryset
