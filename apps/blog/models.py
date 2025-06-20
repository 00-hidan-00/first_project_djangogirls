from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    local_number = models.PositiveIntegerField('Local Number', editable=False, null=True, blank=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    class Meta:
        unique_together = ('post', 'local_number')

    def save(self, *args, **kwargs):
        if not self.pk:
            # New comment — assign local_number
            last = Comment.objects.filter(post=self.post).order_by('-local_number').first()
            self.local_number = (last.local_number + 1) if last else 1
        else:
            # Check if post has changed
            old = Comment.objects.filter(pk=self.pk).first()
            if old and old.post != self.post:
                # Post changed — recalculate local_number
                last = Comment.objects.filter(post=self.post).order_by('-local_number').first()
                self.local_number = (last.local_number + 1) if last else 1
        super().save(*args, **kwargs)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
