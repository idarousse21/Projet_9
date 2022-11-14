from django.conf import settings
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render

from django.views.generic.edit import FormView
from . import forms


class LoginPageView(FormView):
    form_class = forms.LoginForm
    template_name = "authentication/login.html"
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        return super().form_valid(form)


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
    return render(request, "authentication/signup.html", context={"signup": signup})
