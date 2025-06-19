from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View

from apps.blog.models import Post


@method_decorator(login_required, name='dispatch')
class PostPublishView(View):
    """
    View to publish a blog post and notify the user.
    """

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        post = get_object_or_404(Post, pk=pk)
        post.publish()
        messages.info(request, f'Post published: "{post.title}"')
        return redirect('post_detail', pk=pk)
