from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateField(auto_now_add=True)
    update = models.DateField(auto_now=True)

    class Meta:
        ordering = ("created", "body")

    def __str__(self) -> str:
        return f"{self.slug} -> {self.user} - {self.created}"

    def get_absolute_url(self):
        return reverse("home:post_detail", args=[self.pk, self.slug])

    def likes_count(self):
        return self.pvotes.count()

    def user_can_like(self, user):
        user_like = user.uvotes.filter(post=self)
        if user_like.exists():
            return True
        return False


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ucomments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="pcomments")
    is_reply = models.BooleanField(default=False)
    reply = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True, related_name="rcomments"
    )
    body = models.TextField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user} - {self.body[:30]}"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uvotes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="pvotes")

    def __str__(self) -> str:
        return f"{self.user} liked {self.post.slug}"
