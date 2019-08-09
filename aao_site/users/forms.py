from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.password_validation import validate_password

from .validators import validate_email


class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout()
        self.helper.form_show_labels = False
        self.helper.form_show_errors = False
        self.helper.layout = Layout(
            Field('username', placeholder='username'),
            Field('password', placeholder='password'),
            # raw html because no way to submit with btn-outline
            HTML('<input type="submit" name="submit" value="log in" class='
                 '"btn btn btn-outline-primary mt-2" id="button-id-submit">')
        )

    class Meta:
        model = User
        fields = ['username', 'password1']


class UserSignupForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        validators=[validate_email],
        help_text='kept secret and no shitty newsletters')

    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        # overwrite help_text
        self.fields['username'].help_text = 'must be unique and will be public'
        self.fields['password1'].help_text = (
            'not too similar to your other personal information, '
            'at least 8 characters, not common and not entirely numeric')
        # enable registration with one password
        del self.fields['password2']
        self.helper = FormHelper()
        self.helper.layout = Layout()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('email', placeholder='email'),
            Field('username', placeholder='username'),
            Field('password1', placeholder='password'),
            # raw html because no way to submit with btn-outline
            HTML('<input type="submit" name="submit" value="sign up" class='
                 '"btn btn btn-outline-primary mt-2" id="button-id-submit">')
        )

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        validate_password(password1, self.instance)
        return password1

    class Meta:
        model = User
        fields = ['username', 'email', 'password1']
