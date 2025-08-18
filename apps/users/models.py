from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model extending AbstractUser.

    Fields:
    - email: Unique user email for login and contact.
    - favorites: Many-to-many relation to favorite blog posts.
    - is_email_verified: Email verification status.
    - is_banned: Ban status of the user.
    - date_of_birth: Optional user birthdate.
    - last_seen: Timestamp of last activity.
    - last_login_ip: IP address of last login.
    """

    email = models.EmailField(
        unique=True, blank=False, null=False, help_text="User's email address, used for login and communication."
    )
    favorites = models.ManyToManyField(
        "blog.Post",
        blank=True,
        related_name="favorited_by",
        help_text="Select posts that the user has marked as favorites.",
    )
    is_email_verified = models.BooleanField(
        default=False, help_text="Indicates whether the user's email has been verified."
    )
    is_banned = models.BooleanField(default=False, help_text="Flags if the user is banned from accessing the site.")

    date_of_birth = models.DateField(null=True, blank=True, help_text="User's date of birth.")

    last_seen = models.DateTimeField(
        null=True, blank=True, help_text="Timestamp of the user's last activity on the site."
    )
    last_login_ip = models.GenericIPAddressField(
        null=True, blank=True, help_text="IP address from which the user last logged in."
    )

    REQUIRED_FIELDS = ["email"]
