from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=25, label="Nom d’utilisateur")
    password = forms.CharField(
        max_length=25, widget=forms.PasswordInput, label="Mot de passe"
    )


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username",)
