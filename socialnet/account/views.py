from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.


class RegisterUser(View):
    form_class = UserRegisterForm

    def get(self, request):
        form = self.form_class()
        return render(request, "account/register.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd["username"], cd["email"], cd["password"])
            messages.success(request, "user register seccessful", "success")

            return redirect("home:home")
        return render(request, "account/register.html", {"form": form})


class LoginUserForm(View):
    form_class = UserLoginForm
    template = "account/login.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is not None:
                login(request, user)
                messages.success(request, "youlogined successfuly", "success")
                return redirect("home:home")
            messages.error(request, "usernmae or your pass is not correct", "warning")
            return render(request, self.template, {"form": form})
