from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.views import View
from .models import Post, Comment, Vote
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostUpdateForm, CommentForm, CommentReplyForm, PostSearch
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.


class HomeView(View):
    form_class = PostSearch

    def get(self, request):
        posts = Post.objects.all()
        if request.GET.get("search"):
            posts = posts.filter(body__contains=request.GET["search"])

        return render(
            request, "home/index.html", {"posts": posts, "form": self.form_class}
        )


class DetailViewPost(View):
    form_class = CommentForm
    form_class_reply = CommentReplyForm

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.post_ionstans = get_object_or_404(
            Post, pk=kwargs["post_id"], slug=kwargs["post_slug"]
        )
        return super().setup(request, *args, **kwargs)

    def get(self, requset, *args: Any, **kwargs: Any):
        # post1 = get_object_or_404(
        #     Post,
        #     id=post_id,
        #     slug=post_slug,
        # )
        # post2 = Post.objects.get(
        #     id=post_id,
        #     slug=post_slug,
        # )
        comment = self.post_ionstans.posrcomment.filter(is_reply=False)
        can_like = False
        if requset.user.is_authenticated and self.post_ionstans.user_can_like(
            requset.user
        ):
            can_like = True
        return render(
            requset,
            "home/detail.html",
            {
                "post": self.post_ionstans,
                "comments": comment,
                "form": self.form_class,
                "reply_form": self.form_class_reply,
                "can_like": can_like,
            },
        )

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post
            new_comment.save()
            messages.success(request, "comment added", "success")
            return redirect(
                "home:post_detail", self.post_ionstans.id, self.post_ionstans.slug
            )


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
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


class PostAddReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm

    def post(self, request, post_id, comment_id):
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, "your reply submit successful ", "success")
        return redirect("home:post_detail", post.id, post.slug)


class PostLikeView(LoginRequiredMixin, View):

    def get(self, request, post_id):
        post = get_object_or_404(Post, post_id)
        like = Vote.objects.filter(post=post, user=request.user)
        if like.exists():
            messages.error(request, "you liked this post already", "warning")
        else:
            Vote.objects.create(post=post, user=request.user)
            messages.success(request, "like", "success")
        return redirect("home:post_detail", post.id, post.slug)
