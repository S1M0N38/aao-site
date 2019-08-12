import re

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.urls import reverse


class LoginPageTest(TestCase):

    def setUp(self):
        url = reverse('login')
        self.response = self.client.get(url)

    def test_signup_status_code_get(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_template_used(self):
        self.assertTemplateUsed(self.response, 'users/login.html')

    def test_contains_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, AuthenticationForm)


class SuccessfullLoginTest(TestCase):

    fixtures = ['users']

    def setUp(self):
        url = reverse('login')
        user = {
            'username': 'test',
            'password': 'tSPjcAmxeXFY5C4',
        }
        self.response = self.client.post(url, user)
        self.dashboard_url = reverse('dashboard')

    def test_redirection(self):
        self.assertRedirects(self.response, self.dashboard_url)

    def test_user_authenticathed(self):
        self.assertIn('_auth_user_id', self.client.session)


class InvalidLoginTest(TestCase):

    fixtures = ['users']
    url = reverse('login')

    def test_login_status_code(self):
        response = self.client.post(self.url, {})
        self.assertEquals(response.status_code, 200)

    def test_submit_empty_form(self):
        response = self.client.post(self.url, {})
        self.assertFormError(
            response, 'form', 'username', 'This field is required.'
        )
        self.assertFormError(
            response, 'form', 'password', 'This field is required.'
        )

    def test_submit_wrong_credeantial(self):
        data = {
            'username': 'fake_username',
            'password': 'fake_password'
        }
        response = self.client.post(self.url, data)
        self.assertFormError(
            response, 'form', '__all__',
            ('Please enter a correct username and password. '
             'Note that both fields may be case-sensitive.')
        )


class SignupPageTest(TestCase):

    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code_get(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_template_used(self):
        self.assertTemplateUsed(self.response, 'users/signup.html')

    def test_contains_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, UserCreationForm)


class SuccessfullSignupTest(TestCase):

    def setUp(self):
        url = reverse('signup')
        user = {
            'email': 'test@mail.com',
            'username': 'test',
            'password1': 'tSPjcAmxeXFY5C4',
        }
        self.response = self.client.post(url, user)
        self.login_url = reverse('login')

    def test_redirection(self):
        self.assertRedirects(self.response, self.login_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())


class InvalidSignupTest(TestCase):

    fixtures = ['users']
    url = reverse('signup')

    def test_signup_status_code(self):
        response = self.client.post(self.url, {})
        self.assertEquals(response.status_code, 200)

    def test_submit_empty_form(self):
        response = self.client.post(self.url, {})
        self.assertFormError(
            response, 'form', 'email', 'This field is required.'
        )
        self.assertFormError(
            response, 'form', 'username', 'This field is required.'
        )
        self.assertFormError(
            response, 'form', 'password1', 'This field is required.'
        )

    def test_email_already_exists(self):
        data = {
            'username': 'test_test',
            'email': 'test@mail.com',
            'password1': 'this_is_the_test_password_1234'
        }
        response = self.client.post(self.url, data)
        self.assertFormError(
            response, 'form', 'email',
            'A user with that email already exists.'
        )

    def test_username_already_exists(self):
        data = {
            'username': 'test',
            'email': 'test_test@gmail.com',
            'password1': 'this_is_the_test_password_1234'
        }
        response = self.client.post(self.url, data)
        self.assertFormError(
            response, 'form', 'username',
            'A user with that username already exists.'
        )

    def test_weak_password(self):
        data = {
            'username': 'test_test',
            'email': 'test_test@gmail.com',
            'password1': '1234'
        }
        response = self.client.post(self.url, data)
        self.assertFormError(
            response, 'form', 'password1',
            'This password is too common.'
            # not test other errors because it means to test django
        )


class UserActivationTest(TestCase):

    def setUp(self):
        url = reverse('signup')
        user = {
            'email': 'test@mail.com',
            'username': 'test',
            'password1': 'tSPjcAmxeXFY5C4',
        }
        self.response = self.client.post(url, user)
        self.login_url = reverse('login')

    def test_email_sent(self):
        self.assertEqual(
            mail.outbox[0].subject, 'Activate your Against All Odds account.')

    def test_no_activated_user_try_to_login(self):
        # this test is here and not in InvalidLoginTest because
        # the user in the fixtures is_active == True (also use for other
        # apps).
        user = {
            'username': 'test',
            'password': 'tSPjcAmxeXFY5C4'
        }
        response = self.client.post(self.login_url, user)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_valid_activation_link(self):
        link = re.findall('href="([^"]*)"', mail.outbox[0].body)[0]
        self.client.get(link)
        self.assertTrue(User.objects.first().is_active)

    def test_invalid_activation_link(self):
        link = re.findall('href="([^"]*)"', mail.outbox[0].body)[0]
        invalid_link = link[:-7] + 'xxxxx/'
        self.client.get(invalid_link)
        self.assertFalse(User.objects.first().is_active)
