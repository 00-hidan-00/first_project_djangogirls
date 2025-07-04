from django.views.generic import DetailView

from apps.blog.models import Post


class PostDetailView(DetailView):
    """
    Display detailed information about a single Post instance.
    """

    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"
