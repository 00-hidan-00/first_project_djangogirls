import logging

from django.contrib import messages
from django.db import DatabaseError
from django.http import HttpResponse
from django.urls import reverse
from django.utils.timezone import now

from apps.blog.forms import PostForm
from apps.blog.models import Post

logger = logging.getLogger(__name__)


class PostBaseEditMixin:
    """
    Mixin for handling create/update post logic:
    saving, publishing, and user feedback messages.
    """

    PUBLISH_ACTION_NAME: str = "publish"
    is_edit: bool = False
    object: Post

    def form_valid(self, form: PostForm) -> HttpResponse:
        """
        Process valid form: save post instance,
        set author and publish date, handle messages.
        """
        post_object = form.save(commit=False)
        is_publish = self._is_publish_action()

        if getattr(post_object, "author", None) is None:
            post_object.author = self.request.user  # type: ignore[attr-defined]

        if is_publish:
            post_object.published_date = now()
        else:
            post_object.published_date = None

        try:
            post_object.save()
        except DatabaseError:
            logger.exception(f"❌ Error saving post {post_object.pk}")
            self._add_message(self._get_error_message(), level="error")
            return super().form_invalid(form)  # type: ignore[misc]
        except Exception as e:
            logger.exception(f"Unexpected error saving post {getattr(post_object, 'pk', 'unknown')}: {str(e)}")
            self._add_message("❌ An unexpected error occurred while saving the post.", level="error")
            return super().form_invalid(form)  # type: ignore[misc]

        self.object = post_object

        self._add_message(self._get_success_message(post_object, is_publish), level="success")

        return super().form_valid(form)  # type: ignore[misc]

    def get_success_url(self) -> str:
        """Redirect to post detail after successful update."""
        return reverse("blog:post_detail", kwargs={"pk": self.object.pk})

    def _get_success_message(self, post_object: Post, is_publish: bool) -> str:
        """
        Return success message for save.
        Must be implemented in subclasses.
        """
        raise NotImplementedError("You must implement _get_success_message in the subclass")

    def _get_error_message(self) -> str:
        """Return error message."""
        return (
            "❌ Error saving the post. Please try again."
            if self.is_edit
            else "❌ Error creating the post. Please try again."
        )

    def _add_message(self, message: str, level: str = "info") -> None:
        """
        Add a feedback message with given level.
        Levels supported: success, error, info (default).
        """
        level_func_map = {
            "success": messages.success,
            "error": messages.error,
            "info": messages.info,
        }
        level_func = level_func_map.get(level, messages.info)
        level_func(self.request, message)  # type: ignore[attr-defined]

    def _is_publish_action(self) -> bool:
        """Check if the form triggered a publish action."""
        return self.PUBLISH_ACTION_NAME in self.request.POST  # type: ignore[attr-defined]
