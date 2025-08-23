from typing import Any

from django.db.models import QuerySet
from django.utils import timezone
from django.views.generic import ListView

from apps.blog.models import Post
from apps.blog.utils import get_favorite_ids


class PostListView(ListView):
    """
    Display all published blog posts.
    Visible to any user.
    """

    model = Post
    template_name = "blog/post/post_list.html"
    context_object_name = "posts"

    def get_queryset(self) -> QuerySet[Post]:
        """Return only published posts, ordered by newest first."""
        queryset = self.model.objects.filter(published_date__lte=timezone.now()).order_by("-published_date")

        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add `is_favorited` flag to posts."""
        context = super().get_context_data(**kwargs)
        favorite_ids = set(get_favorite_ids(self.request))
        context["page_title"] = "Posts"

        for post in context["posts"]:
            post.is_favorited = post.id in favorite_ids

        return context
