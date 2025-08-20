import logging
from typing import Any

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST

from apps.blog.models import Post

logger = logging.getLogger(__name__)


@method_decorator(require_POST, name="dispatch")
class ToggleFavorite(View):
    """Toggle favorite status of a blog post."""

    object: Post
    post_pk: int

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Get the post object and check if it is published."""
        self.object: Post = get_object_or_404(Post, pk=kwargs.get("pk"))
        self.post_pk = self.object.pk

        if not self.object.is_published:
            messages.error(request, "❌ You are not allowed to add this post to favorites.")
            logger.warning(f"User {request.user.id} tried to add this post to favorites {self.post_pk}.")
            return self.redirect_back()

        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Toggle favorite status of the post."""

        if request.user.is_authenticated:
            try:
                if request.user.has_favorited(post=self.object):
                    request.user.unfavorite(self.object)
                    logger.info(
                        f"User {request.user.username} (ID {request.user.id})"
                        f" removed post {self.post_pk} from favorites."
                    )
                else:
                    request.user.favorite(self.object)
                    logger.info(
                        f"User {request.user.username} (ID {request.user.id}) added post {self.post_pk} to favorites."
                    )
            except Exception as e:
                logger.error(f"Failed to toggle favorite for user {request.user.id}: {e}")
                messages.error(request, "⚠️ Something went wrong while updating favorites.")

        else:
            try:
                favorites = [int(i) for i in request.session.get("post_favorites", [])]
            except ValueError:
                logger.warning("Corrupted session data in post_favorites, resetting.")
                favorites = []
            if self.post_pk in favorites:
                favorites.remove(self.post_pk)
                logger.info(f"Anonymous user removed post {self.post_pk} from session favorites.")

            else:
                favorites.append(self.post_pk)
                logger.info(f"Anonymous user added post {self.post_pk} to session favorites.")

            request.session["post_favorites"] = favorites

        return self.redirect_back()

    def redirect_back(self):
        return redirect(self.request.META.get("HTTP_REFERER", "/"))
