import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from apps.blog.forms import PostForm
from apps.blog.mixins import PostBaseEditMixin
from apps.blog.models import Post

logger = logging.getLogger(__name__)


class PostNewView(LoginRequiredMixin, PostBaseEditMixin, CreateView):
    """
    View to create a new blog post.
    Only authenticated users can access this page.
    """

    model = Post
    form_class = PostForm
    template_name = "blog/post/post_edit.html"
    context_object_name = "post"

    is_edit = False

    def _get_success_message(self, blog_post: Post, is_publish: bool) -> str:
        """Return success message for save."""
        if is_publish:
            logger.info(f'Post "{blog_post.title}" (ID {blog_post.pk}) published by user {blog_post.author.username}')
            message = f'🎉 Post published: "{blog_post.title}"'
        else:
            logger.info(
                f'Post "{blog_post.title}" (ID {blog_post.pk}) saved as draft by user {blog_post.author.username}'
            )
            message = f'💾 Post created and saved as draft: "{blog_post.title}"'
        return message
