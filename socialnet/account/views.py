from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib import messages

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
            User.objects.create_user(
                username=cd["username"], email=cd["eamil"], password=cd["password"]
            )
            messages.success(request, "user register seccessful", "success")

            return redirect("home:home")
        return render(request, "account/register.html", {"form": form})
