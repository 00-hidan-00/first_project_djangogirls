from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.blog.models import Comment, Post
from apps.users.models import User


class PostDetailViewTest(TestCase):
    def setUp(self):
        # Users
        self.user = User.objects.create_user(username="denis", password="123", email="denis@test.com")
        self.superuser = User.objects.create_superuser(username="admin", password="123", email="admin@test.com")
        self.other_user = User.objects.create_user(username="bob", password="123", email="bob@test.com")

        # Posts
        self.post_published = Post.objects.create(
            title="Published",
            text="Some text",
            author=self.user,
            published_date=timezone.now(),
        )
        self.post_draft = Post.objects.create(
            title="Draft",
            text="Draft text",
            author=self.user,
            published_date=None,
        )

        # Comments
        self.comment_visible = Comment.objects.create(
            post=self.post_published,
            author=self.user,
            text="Visible",
            approved_comment=True,
        )
        self.comment_hidden = Comment.objects.create(
            post=self.post_published,
            author=self.user,
            text="Hidden",
            approved_comment=False,
        )

    # --- Post access ---
    def test_published_post_accessible(self):
        """Published post is accessible to everyone"""
        url = reverse("blog:post_detail", args=[self.post_published.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Published")

    def test_draft_accessible_for_author(self):
        """Author can view their own draft"""
        self.client.login(username="denis", password="123")
        url = reverse("blog:post_detail", args=[self.post_draft.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Draft")

    def test_draft_accessible_for_superuser(self):
        """Superuser can view drafts"""
        self.client.login(username="admin", password="123")
        url = reverse("blog:post_detail", args=[self.post_draft.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_draft_redirects_for_other_users(self):
        """Other users are redirected from drafts"""
        self.client.login(username="bob", password="123")
        url = reverse("blog:post_detail", args=[self.post_draft.pk])
        response = self.client.get(url)
        self.assertRedirects(response, reverse("blog:post_list"))
        # Check the message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("You do not have permission" in str(m) for m in messages))

    # Context and comments
    def test_context_includes_visible_comments(self):
        """Only visible comments are included in context"""
        url = reverse("blog:post_detail", args=[self.post_published.pk])
        response = self.client.get(url)
        visible_comments = response.context["visible_comments"]
        self.assertIn(self.comment_visible, visible_comments)
        self.assertNotIn(self.comment_hidden, visible_comments)

    # --- Флаг избранного ---
    def test_is_favorited_flag_for_authenticated_user(self):
        """is_favorited flag works for authenticated user"""
        self.client.login(username="denis", password="123")
        self.user.favorites.add(self.post_published)
        url = reverse("blog:post_detail", args=[self.post_published.pk])
        response = self.client.get(url)
        post = response.context["post"]
        self.assertTrue(post.is_favorited)

    def test_is_favorited_flag_for_anonymous_user(self):
        """is_favorited flag works for anonymous user via session"""
        session = self.client.session
        session["post_favorites"] = [self.post_published.id]
        session.save()
        url = reverse("blog:post_detail", args=[self.post_published.pk])
        response = self.client.get(url)
        post = response.context["post"]
        self.assertTrue(post.is_favorited)
