from typing import Any

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.http import HttpRequest

from apps.blog.models import Post
from apps.users.models import User


@receiver(user_logged_in)
def merge_favorites_on_login(sender: Any, user: User, request: HttpRequest, **kwargs: Any) -> None:
    """
    Signal triggered when a user logs in.
    Transfers favorite posts from the session to the logged-in user's favorites.
    """

    session_favorites = request.session.pop("post_favorites", [])
    if not session_favorites:
        return
    favorite_ids = {int(post_id) for post_id in session_favorites}

    posts = Post.objects.filter(id__in=favorite_ids)
    for post in posts:
        if not user.has_favorited(post):
            user.favorite(post)

    print("SIGNAL TRIGGERED", favorite_ids)
