from django.contrib import admin

from .models import Post, Comment


# admin.site.register(Post)
# admin.site.register(Comment)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment
