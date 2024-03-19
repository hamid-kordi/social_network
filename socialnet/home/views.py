from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostUpdateForm

# Create your views here.


class HomeView(View):

    def get(self, request):
        posts = Post.objects.all()
        return render(request, "home/index.html", {"posts": posts})


class DetailViewPost(View):
    def get(self, requset, post_id, post_slug):
        post = Post.objects.get(id=post_id, slug=post_slug)
        return render(requset, "home/detail.html", {"post": post})


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, "post deleted successfuly", "success")
        else:
            messages.error(request, "you can not delete the post", "danger")
        return redirect("home:home")


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostUpdateForm

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        post = Post.objects.get(pk=kwargs['post_id'])
        if not post.user.id == request.user.id:
            messages.error(request, "you can not update post", "danger")
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_id):
        post = Post.objects.get(pk = user_id)
        form = self.form_class(isinstance=post)
        return render(request, "home/update.html", {"form": form})
