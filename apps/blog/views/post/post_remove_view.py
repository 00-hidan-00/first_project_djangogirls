from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from apps.blog.models import Post


@login_required
def post_remove(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        if post:
            messages.warning(request, f"Post deleted: {post.title}")
        else:
            messages.info(request, "Nothing deleted")
    return redirect('post_list')
