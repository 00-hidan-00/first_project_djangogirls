import logging
from smtplib import SMTPException

from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.core.mail import BadHeaderError
from django.http import HttpResponse
from django.urls import reverse_lazy

logger = logging.getLogger(__name__)


class UserPasswordResetView(PasswordResetView):
    """
    Custom password reset view that shows a success message
    and logs the reset request.
    """

    email_template_name = "registration/reset/password_reset_email.html"
    template_name = "registration/reset/password_reset_form.html"
    success_url = reverse_lazy("blog:post_list")

    def form_valid(self, form: PasswordResetForm) -> HttpResponse:
        """
        If the form is valid, try sending the password reset email.
        Log the request, handle errors gracefully.
        """
        email = form.cleaned_data["email"]

        try:
            response = super().form_valid(form)
        except (SMTPException, BadHeaderError, Exception) as e:
            logger.exception(f"❌ Failed to send password reset email to {email}: {e}")
            messages.error(self.request, "❌ Error sending password reset email. Please try again later.")
            return self.render_to_response(self.get_context_data(form=form))

        logger.info(f"Password reset requested for email: {email}")
        messages.success(self.request, "📧 Password reset link was sent to your email.")

        return response

    def form_invalid(self, form: PasswordResetForm) -> HttpResponse:
        """If the form is invalid (e.g. bad email format), log the issue and show an error message to the user."""
        messages.error(self.request, "⚠️ Please correct the errors below.")
        logger.warning("Password reset form is invalid. Errors: %s", form.errors)

        return super().form_invalid(form)
