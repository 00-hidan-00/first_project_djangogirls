from django.contrib import admin

from .models import Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post

    # Fields to display in the list view
    list_display = ("title", "author", "created_date", "published_date")

    # Fields you can filter by in the sidebar
    list_filter = ("created_date", "published_date", "author")

    # Fields to search by
    search_fields = ("title", "text", "author__username")

    # Automatically fill the 'author' field with the current user (optional)
    # def save_model(self, request, obj, form, change):
    #     if not obj.pk:
    #         obj.author = request.user
    #     super().save_model(request, obj, form, change)

    # Date hierarchy navigation in admin
    date_hierarchy = "created_date"

    # Order by default
    ordering = ("-created_date",)

    # Fields layout in the admin form
    fieldsets = (
        (None, {"fields": ("author", "title", "text")}),
        ("Dates", {"fields": ("created_date", "published_date")}),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment

    # Fields to display in the list view
    list_display = (
        "id",
        "post",
        "author",
        "local_number",
        "approved_comment",
        "created_date",
    )

    # Fields you can filter by in the sidebar
    list_filter = ("approved_comment", "created_date", "post")

    # Fields to search by
    search_fields = ("author", "text", "post__title")

    # Read-only fields
    readonly_fields = ("local_number", "created_date")

    # Fields layout in the admin form
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "post",
                    "author",
                    "text",
                    "approved_comment",
                    "local_number",
                    "created_date",
                )
            },
        ),
    )

    # Optional: Add approve action in list view (custom button)
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        updated = queryset.update(approved_comment=True)
        self.message_user(request, f"{updated} comments approved.")

    approve_comments.short_description = "Approve selected comments"  # type: ignore[attr-defined]
