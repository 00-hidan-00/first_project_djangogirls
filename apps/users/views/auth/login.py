import logging
from typing import Any

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy

from apps.users.models import User

logger = logging.getLogger(__name__)


class UserLoginView(LoginView):
    """Handle user login with feedback messages and logging."""

    template_name = "registration/login.html"
    success_url = reverse_lazy("blog:post_list")

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Redirect already logged-in users with info message."""
        if request.user.is_authenticated:
            messages.info(request, "👀 You are already logged in.")
            return redirect("blog:post_list")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        """Log in the user, show message, and log the event."""
        user: User = form.get_user()

        messages.success(self.request, f"🎉 Welcome back, {user.username}!")
        logger.info(f"User {user.username} logged in successfully.")

        return super().form_valid(form)

    def form_invalid(self, form: AuthenticationForm) -> HttpResponse:
        """Show error message, log failed login attempt when form data is invalid."""
        messages.error(self.request, "❌ Invalid username or password.")
        logger.warning(f"Failed login attempt for username: {form.data.get('username')}")

        return super().form_invalid(form)
