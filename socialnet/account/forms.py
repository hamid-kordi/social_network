from typing import Any
from django import forms
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError


class UserRegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "your password"}
        )
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        user = User.objects.filter(email=email).exists() #return true or false
        if user:
            raise ValidationError("this emial exist !")
        return email
