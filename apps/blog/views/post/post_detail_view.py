from typing import Any

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import DetailView

from apps.blog.models import Post


class PostDetailView(DetailView):
    """
    Display a single blog post with its comments.
    Drafts are visible only to the author or a superuser.
    """

    model = Post
    template_name = "blog/post/post_detail.html"
    context_object_name = "post"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Restrict access to drafts. Only author or superuser may view them."""
        self.object = self.get_object()
        user = request.user

        if self.object.is_published is False and not self.object.is_visible_to(user):
            messages.error(request, "❌ You do not have permission to view this draft post.")
            return redirect("blog:post_list")

        context = self.get_context_data(object=self.object)

        return self.render_to_response(context)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add visible comments to context based on user permissions."""
        context = super().get_context_data(**kwargs)
        context["visible_comments"] = self.object.visible_comments_for(self.request.user).order_by("created_date")

        if self.object.is_published:
            return context

        if self.request.user.is_authenticated:
            favorite_ids = set(self.request.user.favorites.values_list("id", flat=True))
        else:
            favorite_ids = set(self.request.session.get("post_favorites", []))

        self.object.is_favorited = self.object.id in favorite_ids

        return context
