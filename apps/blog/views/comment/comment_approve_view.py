from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View

from apps.blog.models import Comment


@method_decorator(login_required, name='dispatch')
class CommentApproveView(View):
    """
    View to approve a comment by its primary key.
    Requires user to be logged in.
    Handles POST requests only.
    """

    def post(self, request: HttpRequest, pk: int, local_number: int, *args, **kwargs) -> HttpResponse:
        comment = get_object_or_404(Comment, post__pk=pk, local_number=local_number)
        comment.approve()
        return redirect('blog:post_detail', pk=comment.post.pk)
