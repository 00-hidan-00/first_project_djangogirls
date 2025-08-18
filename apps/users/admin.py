from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Fields displayed in the list view
    list_display = (
        "username",
        "email",
        "is_email_verified",
        "is_banned",
        "is_staff",
        "is_superuser",
        "last_login",
        "last_seen",
    )

    # Filters displayed in the right sidebar
    list_filter = ("is_staff", "is_superuser", "is_banned", "is_email_verified", "groups")

    # Fields searchable via the admin search bar
    search_fields = ("username", "email")

    # Default ordering of user list
    ordering = ("-date_joined",)

    # Fields shown in the user edit view
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("email", "date_of_birth")}),
        (_("Activity"), {"fields": ("last_seen", "last_login_ip")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_email_verified",
                    "is_banned",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    # Fields shown when creating a new user in the admin
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )
