from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateField(auto_now_add=True)
    update = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.slug} -> {self.user} - {self.created}"

    def get_absolute_url(self):
        return reverse('home:post_detail',args=[self.id,self.slug])