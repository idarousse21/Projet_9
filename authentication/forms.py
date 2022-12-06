from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from . import models


class LoginForm(forms.ModelForm):
    identifier = forms.CharField(
        max_length=25,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"}),
    )
    password = forms.CharField(
        max_length=25,
        label="",
        widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe"}),
    )

    class Meta:
        model = models.User
        fields = ["identifier", "password"]


class SignupForm(UserCreationForm):
    username = forms.CharField(
        max_length=25,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"}),
    )
    password1 = forms.CharField(
        max_length=25,
        label="",
        widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe"}),

    )
    password2 = forms.CharField(
        max_length=25,
        label="",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirmation du mot de passe"}
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "password1", "password2")
