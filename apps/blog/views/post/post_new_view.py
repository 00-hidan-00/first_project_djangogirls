from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.timezone import now
from django.views.generic import CreateView

from apps.blog.forms import PostForm
from apps.blog.models import Post


class PostNewView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_edit.html"
    context_object_name = "post"

    PUBLISH_ACTION_NAME = "publish"

    def form_valid(self, form: PostForm) -> HttpResponseRedirect:
        """
        Handle valid form submission.
        Save post with author and published_date (if publishing).
        Add user message about the action.
        """
        post: Post = form.save(commit=False)
        post.author = self.request.user

        if self._is_publish_action():
            post.published_date = now()
            self._add_message(f'Post created: "{post.title}"', success=True)
        else:
            self._add_message(f'Post saved as draft: "{post.title}"', success=True)

        post.save()
        self.object = post
        return super().form_valid(form)

    def get_success_url(self) -> str:
        """Return URL to redirect after successful form submission."""
        return reverse("blog:post_detail", kwargs={"pk": self.object.pk})

    def _is_publish_action(self) -> bool:
        """Check if the form submission corresponds to a publish action."""
        return self.PUBLISH_ACTION_NAME in self.request.POST

    def _add_message(self, message: str, success: bool = False) -> None:
        """Add a message to be displayed to the user."""
        if success:
            messages.success(self.request, message)
        else:
            messages.info(self.request, message)
