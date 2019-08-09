from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView

from .forms import UserLoginForm, UserSignupForm


class LoginPage(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm


class LogoutPage(LogoutView):
    ...


class SignupPage(CreateView):
    template_name = 'users/signup.html'
    form_class = UserSignupForm
    success_url = reverse_lazy('login')
