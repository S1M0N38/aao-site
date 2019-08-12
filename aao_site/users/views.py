from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic.edit import CreateView

from .forms import UserLoginForm, UserSignupForm
from .tokens import account_activation_token


class LoginPage(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm


class LogoutPage(LogoutView):
    ...


class SignupPage(CreateView):
    template_name = 'users/signup.html'
    form_class = UserSignupForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()
        self.send_email(self.object)
        success_msg = ('An email was set to your address with the link '
                       'for account activation.')
        messages.success(self.request, success_msg)
        return redirect(self.get_success_url())

    def send_email(self, user):
        subject = 'Activate your Against All Odds account.'
        data = {
            'user': user,
            'request': self.request,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }
        message = render_to_string('users/email_activation.html', data)
        email = EmailMessage(subject, message, to=[user.email])
        email.content_subtype = 'html'
        email.send()


def ActivatePage(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        success_msg = 'Your account is now activated.'
        messages.success(request, success_msg)
        return redirect('login')
    else:
        warning_msg = 'The activation link is expired or invalid.'
        messages.warning(request, warning_msg)
        return redirect('home')
