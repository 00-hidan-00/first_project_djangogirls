import logging
from typing import Any

from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.core.exceptions import ValidationError as CoreValidationError
from django.forms import ValidationError as FormsValidationError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy

from apps.users.models import User

logger = logging.getLogger(__name__)


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Custom view to confirm password reset using the reset link.
    Displays messages on success or invalid links.
    """

    template_name = "registration/reset/password_reset_confirm.html"
    success_url = reverse_lazy("blog:post_list")

    def render_to_response(self, context: dict[str, Any], **response_kwargs: Any) -> HttpResponse:
        """If the reset link is invalid, redirect with an error message."""
        if not context.get("validlink", False):
            messages.error(self.request, "⚠️ The password reset link is invalid or has expired.")
            return redirect(self.success_url)
        return super().render_to_response(context, **response_kwargs)

    def form_valid(self, form: SetPasswordForm) -> HttpResponse:
        """Handle a valid password reset form: show success message, log the event, handle exceptions."""
        user: User = form.user

        try:
            response = super().form_valid(form)
        except (CoreValidationError, FormsValidationError):
            messages.error(self.request, "❌ There was an error validating your password. Please try again.")
            logger.error(f"Validation error when resetting password for user {user.username} (ID {user.id}) ")
            return self.render_to_response(self.get_context_data(form=form))
        except Exception as e:
            messages.error(self.request, "❌ Unexpected error occurred. Please try again later.")
            logger.exception(f"Unexpected error resetting password for user {user.username} (ID {user.id}): {e} ")
            return self.render_to_response(self.get_context_data(form=form))

        messages.success(self.request, "✅ Your password has been successfully changed.")
        logger.info(f"Password successfully changed for user: {user.username} (ID {user.id})")

        return response

    def form_invalid(self, form: SetPasswordForm) -> HttpResponse:
        """Handle an invalid password reset form: show error message and log the issue."""
        username = getattr(form.user, "username", "unknown")
        messages.error(self.request, "⚠️ Please correct the errors below.")
        logger.warning(f"Password reset confirm form invalid for user '{username}'" f"Errors: {form.errors.as_json()}")

        return super().form_invalid(form)
