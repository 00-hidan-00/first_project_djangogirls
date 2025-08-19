from django.shortcuts import render

from apps.blog.models import Post


def favorite_posts(request):
    if request.user.is_authenticated:
        posts = request.user.favorites.all()
        favorite_ids = set(request.user.favorites.values_list("id", flat=True))
    else:
        favorite_ids = request.session.get("post_favorites", [])
        posts = Post.objects.filter(id__in=favorite_ids)

    for post in posts:
        post.is_favorited = post.id in favorite_ids

    return render(request, "blog/post/post_favorite_list.html", {"posts": posts})
