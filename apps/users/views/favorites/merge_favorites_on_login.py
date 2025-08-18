from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from apps.blog.models import Post


@receiver(user_logged_in)
def merge_favorites_on_login(sender, user, request, **kwargs):
    session_favorites = request.session.get("favorites", [])
    for post_id in session_favorites:
        try:
            post = Post.objects.get(id=post_id)
            user.favorites.add(post)
        except Post.DoesNotExist:
            pass
    request.session["favorites"] = []
