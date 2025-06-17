from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from apps.blog.models import Comment


@login_required
def comment_approve(request: HttpRequest, pk: int) -> HttpResponse:
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)
