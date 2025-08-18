from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.views.generic import ListView

from apps.blog.models import Post


class PostDraftListView(LoginRequiredMixin, ListView):
    """
    Display all draft posts for the current user.
    Only the author or a superuser may access this page.
    """

    model = Post
    template_name = "blog/post/post_draft_list.html"
    context_object_name = "posts"

    def get_queryset(self) -> QuerySet[Post]:
        """Return draft posts for the current user or all if superuser."""
        user = self.request.user
        queryset = Post.objects.filter(published_date__isnull=True)

        if not user.is_superuser:
            queryset = queryset.filter(author=user)

        return queryset.order_by("-created_date")
