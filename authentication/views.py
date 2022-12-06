from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.conf import settings
from . import forms


def logout_user(request):
    logout(request)
    return redirect(settings.LOGIN_URL)


def signup_page(request):
    signup = forms.SignupForm()
    if request.method == "POST":
        signup = forms.SignupForm(request.POST)
        if signup.is_valid():
            user = signup.save()
            login(request, user)
            return redirect(settings.LOGIN_URL)
    return render(
        request,
        "authentication/signup.jinja2",
        context={
            "signup": signup})
