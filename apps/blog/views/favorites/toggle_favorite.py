from django.shortcuts import get_object_or_404, redirect

from apps.blog.models import Post


def toggle_favorite(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user.is_authenticated:
        if request.user.has_favorited(post=post):
            request.user.unfavorite(post)
        else:
            request.user.favorite(post)

    else:
        favorites = request.session.get("post_favorites", [])
        if post_id in favorites:
            favorites.remove(post_id)
        else:
            favorites.append(post_id)
        request.session["post_favorites"] = favorites

    return redirect(request.META.get("HTTP_REFERER", "/"))
