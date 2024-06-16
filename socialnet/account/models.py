from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Follow(models.Model):
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="folloing")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.from_user} following {self.to_user}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(default=0)
    bio = models.TextField(null=True,blank=True)