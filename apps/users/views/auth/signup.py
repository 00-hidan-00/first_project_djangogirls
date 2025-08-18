import logging
from typing import Any

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.users.forms import CustomUserCreationForm
from apps.users.models import User

logger = logging.getLogger(__name__)


class SignUpView(CreateView):
    """
    Handle user registration.
    Redirect authenticated users away.
    """

    model = User
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("account:login")

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Redirect already registered users with info message."""
        if request.user.is_authenticated:
            messages.info(request, "👀 You are already registered and logged in.")
            return redirect("blog:post_list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: CustomUserCreationForm) -> HttpResponse:
        """Register user, show message, and log the event."""
        user = form.save()
        messages.success(self.request, "🎉 Account created successfully. Please log in.")
        logger.info(f"New user registered: {user.username} (ID {user.id})")
        return super().form_valid(form)

    def form_invalid(self, form: CustomUserCreationForm) -> HttpResponse:
        logger.warning(f"Invalid signup attempt. Errors: {form.errors.as_json()}")
        messages.error(self.request, "❌ Please correct the errors below.")
        return super().form_invalid(form)
