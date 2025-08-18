from django.shortcuts import render

from apps.blog.models import Post


def favorite_posts(request):
    if request.user.is_authenticated:
        posts = request.user.favorites.all()
    else:
        fav_ids = request.session.get("", [])
        posts = Post.objects.filter(id__in=fav_ids)
    return render(request, "blog/post/post_list.html", {"posts": posts})
