from unittest import skip

from .utils import StaticLiveServerTestCaseSelenium


# Sam now want to start to use aao, so he click on dashboard and a wild login
# page appeared.

@skip('Not implemented yet')
class LoginPageTest(StaticLiveServerTestCaseSelenium):

    def test_login_wrong_credentials(self):
        # He try to login with some credentials that he use also for other
        # website; maybe he have already an account and he doesn't remeber
        # his past.
        ...

    def test_login_right_credentials(self):
        # No, he doesn't have an account. He ask a friend to borrow an
        # account in order to take a quick glance to aao dashbord.
        ...


# He conclude that aao have some potential so he decided to make a personal
# account.

class SignupPageTest(StaticLiveServerTestCaseSelenium):

    def test_link_to_signup_page(self):
        # At the bottom of the login he saw the link to the signup so he
        # click it.
        ...

    def test_invalid_form_compilation(self):
        # He does't compile the form correctly and he get an error message.
        ...

    def test_username_already_chosen(self):
        # He have chosen a too common username: test. The form is not valid
        # yet so he have to choose another username.
        ...

    def test_valid_form_compilation(self):
        # Finally. He signup procedure is subimt! :)
        ...


# Now just a final step: he have to conferm his email in order to complete
# the registration process.

@skip('Not implemented yet')
class EmailConfermationTest(StaticLiveServerTestCaseSelenium):

    def test_invalid_email_confermation(self):
        # He forget to conferm his email so he can't access to the dashboard
        ...

    def test_valid_email_confermation(self):
        # Now he caw he can to login into dashboard and use other aao features
        # like the(REST-API and the python wrapper
        ...


# A issue rise: he doesn't remeber his password.
# He have to make a password reset. :(

@skip('Not implemented yet')
class TestPasswordReset(StaticLiveServerTestCaseSelenium):

    def test_link_to_send_email_for_password_reset(self):
        # In order to reset his password he click the "password_reset" link
        # An email was sent and he see a message at the bottom of the page:
        # "check out your email inbox, the link for password reset was sent"
        ...

    def test_password_reset_link(self):
        # He check his inbox, see the email and click on the reset link.
        # He is redirect to the password reset page
        ...

    def test_password_reset_form(self):
        # He input the new password and click on submit.
        # He is redirect to login page and see a message that conferm that
        # the password reset procedure was sucessful.
        ...
