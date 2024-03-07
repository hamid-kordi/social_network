from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .forms import UserRegisterForm

# Create your views here.


class RegisterUser(View):


    def get(self, request):
        form = UserRegisterForm()
        return render(request, "account/register.html", {'form': form})

    def post(self, request):
        return render(request, "")
