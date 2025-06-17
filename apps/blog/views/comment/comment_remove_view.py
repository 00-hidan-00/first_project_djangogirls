from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from apps.blog.models import Comment


@login_required
def comment_remove(request: HttpRequest, pk: int) -> HttpResponse:
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    if comment:
        messages.warning(request, f"Comment deleted: {comment.text}")
    else:
        messages.info(request, "Nothing deleted")
    return redirect('post_detail', pk=comment.post.pk)
