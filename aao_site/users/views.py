from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from .forms import UserSignupForm


class LoginPage(TemplateView):
    template_name = 'users/login.html'


class SignupPage(CreateView):
    template_name = 'users/signup.html'
    form_class = UserSignupForm
    success_url = reverse_lazy('login')
