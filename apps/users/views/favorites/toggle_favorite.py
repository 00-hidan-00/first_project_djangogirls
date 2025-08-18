from django.shortcuts import get_object_or_404, redirect

from apps.blog.models import Post


def toggle_favorite(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user.is_authenticated:
        # Работа с базой
        if post in request.user.favorites.all():
            request.user.favorites.remove(post)
        else:
            request.user.favorites.add(post)
    else:
        # Работа с сессией
        favorites = request.session.get("", [])
        if post_id in favorites:
            favorites.remove(post_id)
        else:
            favorites.append(post_id)
        request.session["favorites"] = favorites

    return redirect(request.META.get("HTTP_REFERER", "/"))
