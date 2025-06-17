from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from apps.blog.models import Post


def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
