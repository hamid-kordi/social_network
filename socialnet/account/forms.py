from typing import Any
from django import forms
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError


class UserRegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        label="passwword",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    password_confirm = forms.CharField(
        label="confirm",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        user = User.objects.filter(email=email).exists()  # return true or false
        if user:
            raise ValidationError("this emial exist !")
        return email

    def clean(self):
        cd = super().clean()
        p1 = cd.get("password")
        p2 = cd.get("password_confirm")
        if p1 and p2 and p1 != p2:
            raise ValidationError("password most be like together")


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
