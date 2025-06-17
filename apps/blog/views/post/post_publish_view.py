from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from apps.blog.models import Post


@login_required
def post_publish(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.publish()
    messages.info(request, f'Pust published: {post.title}')
    return redirect('post_detail', pk=pk)
