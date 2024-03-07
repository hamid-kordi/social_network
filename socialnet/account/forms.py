from django import forms


class UserRegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(widget=forms.EmailInput(attr={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "your password"}
        )
    )
