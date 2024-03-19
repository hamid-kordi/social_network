from django import forms
from .models import Post


class PostUpdateForm(forms.Form):
    class Meta:
        models = Post
        field = ("body",)
