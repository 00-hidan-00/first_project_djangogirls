from typing import Any

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView

from apps.blog.models import Post
from apps.blog.utils import get_favorite_ids


class PostFavoriteListView(ListView):
    """
    Display all favorited blog posts.
    """

    model = Post
    template_name = "blog/post/post_favorite_list.html"
    context_object_name = "posts"

    favorite_ids: set[int]

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Initialize favorite IDs from the request."""
        self.favorite_ids = set(get_favorite_ids(request))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Post]:
        """Return favorited posts queryset."""
        if self.request.user.is_authenticated:
            return Post.objects.filter(favorited_by=self.request.user).order_by("-published_date")
        return Post.objects.filter(id__in=self.favorite_ids).order_by("-published_date")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add `is_favorited` flag to posts."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Draft Posts"

        for post in context["posts"]:
            post.is_favorited = True

        return context
