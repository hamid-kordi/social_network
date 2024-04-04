from typing import Any
from django.shortcuts import render, redirect,get_list_or_404
from django.http import HttpRequest, HttpResponse
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostUpdateForm
from django.utils.text import slugify

# Create your views here.


class HomeView(View):

    def get(self, request):
        posts = Post.objects.all()
        return render(request, "home/index.html", {"posts": posts})


class DetailViewPost(View):
    def get(self, requset, post_id, post_slug):
        post = get_list_or_404(Post,id=post_id, slug=post_slug,)
       
        return render(requset, "home/detail.html", {"post": post})


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_list_or_404(Post,id=post_id)
        # post = Post.objects.get(pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, "post deleted successfuly", "success")
        else:
            messages.error(request, "you can not delete the post", "danger")
        return redirect("home:home")


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostUpdateForm

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.post_instanse = Post.objects.get(pk=kwargs["post_id"])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        post = self.post_instanse
        if not post.user.id == request.user.id:
            messages.error(request, "you can not update post", "danger")
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instanse
        form = self.form_class(instance=post)
        return render(request, "home/update.html", {"form": form})

    def post(self, request, *args, **kwargs):
        post = self.post_instanse
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data["body"][:30])
            new_post.save()
            messages.success(request, "post changed successfuly", "success")
            return redirect("home:post_detail", post.id, post.slug)


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostUpdateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, "home/create.html", {"form": form})
        

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data["body"][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, "post create successfuly", "success")
            return redirect("home:post_detail", new_post.id, new_post.slug)
