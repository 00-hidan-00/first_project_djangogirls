from django.urls import include, path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("post/new/", views.PostNewView.as_view(), name="post_new"),
    path("drafts/", views.PostDraftListView.as_view(), name="post_draft_list"),
    path(
        "post/<int:pk>/",
        include(
            [
                path("", views.PostDetailView.as_view(), name="post_detail"),
                path("edit/", views.PostEditView.as_view(), name="post_edit"),
                path("publish/", views.PostPublishView.as_view(), name="post_publish"),
                path("remove/", views.PostRemoveView.as_view(), name="post_remove"),
                path("comment/", views.AddCommentToPostView.as_view(), name="add_comment_to_post"),
                path(
                    "comment/<int:local_number>/",
                    include(
                        [
                            path("approve/", views.CommentApproveView.as_view(), name="comment_approve"),
                            path("remove/", views.CommentRemoveView.as_view(), name="comment_remove"),
                        ]
                    ),
                ),
            ]
        ),
    ),
]
