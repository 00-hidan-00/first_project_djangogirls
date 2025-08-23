import logging

from django.contrib import messages
from django.http import HttpRequest

from apps.blog.models import Comment

logger = logging.getLogger(__name__)


def log_comment_action(request: HttpRequest, comment: Comment, action: str) -> None:
    """Logs and sends a message for comment actions (approve/delete)."""

    comment_text = comment.text[:20] + "…" if len(comment.text) > 20 else comment.text

    logger.info(
        f"Comment {action} by user {request.user.username} (ID: {request.user.pk}) "
        f'to post "{comment.post.title}" (ID: {comment.post.pk}): "{comment_text}"'
    )

    if action == "deleted":
        messages.warning(request, f'🗑️ Comment deleted: "{comment_text}"')
    elif action == "approved":
        messages.success(request, f'✅ Comment approved: "{comment_text}"')
