from unittest import skip

from .utils import StaticLiveServerTestCaseSelenium


# Sam now want to start to use aao, so he click on dashboard and a wild login
# page appeared.


class LoginPageTest(StaticLiveServerTestCaseSelenium):

    @property
    def url(self):
        return f'{self.live_server_url}/login/'

    def test_login_wrong_credentials(self):
        # He try to login with some credentials that he use also for other
        # website; maybe he have already an account and he doesn't remeber
        # his past.
        self.browser.get(self.url)
        self.compile_login_form('fake_username', 'fake_password')
        self.assertEqual(self.browser.current_url, self.url)
        error_msg = self.browser.find_element_by_tag_name('p').text
        self.assertEqual(error_msg, 'Incorrect username and password.')
        # A message appears: "wronng credentials"
        msg = self.browser.find_element_by_xpath(
            '//div[@class="alert alert-danger mt-4"]').text
        self.assertEqual(msg, 'Incorrect username and password.')

    def test_login_right_credentials(self):
        # No, he doesn't have an account. He ask a friend to borrow an
        # account in order to take a quick glance to aao dashbord.
        self.browser.get(self.url)
        self.compile_login_form('test', 'tSPjcAmxeXFY5C4')
        self.assertEqual(
            self.browser.current_url, f'{self.live_server_url}/dashboard/')


# He conclude that aao have some potential so he decided to make a personal
# account.


class SignupPageTest(StaticLiveServerTestCaseSelenium):

    @property
    def url(self):
        return f'{self.live_server_url}/signup/'

    def test_link_to_signup_page(self):
        # At the bottom of the login he saw the link to the signup so he
        # click it.
        self.browser.get(f'{self.live_server_url}/login/')
        self.browser.find_elements_by_tag_name('a')[1].click()
        self.assertEqual(self.browser.current_url, self.url)

    def test_submit_empty_form(self):
        # He try to submit the empty form but obviously nothing happens
        self.browser.get(self.url)
        self.compile_signup_form('', '', '')
        self.assertEqual(self.browser.current_url, self.url)

    def test_email_already_exists(self):
        # He have chosen a too common username: test. The form is not valid
        # yet so he have to choose another username.
        self.browser.get(self.url)
        self.compile_signup_form('test@mail.com', 'test_test', 'md934y91us1')
        error_msg = self.browser.find_element_by_class_name(
            'invalid-feedback').text
        self.assertEqual(error_msg, 'A user with that email already exists.')

    def test_username_already_exists(self):
        # He have chosen a too common username: test. The form is not valid
        # yet so he have to choose another username.
        self.browser.get(self.url)
        self.compile_signup_form('test_test@mail.com', 'test', 'md934y91us1')
        error_msg = self.browser.find_element_by_class_name(
            'invalid-feedback').text
        self.assertEqual(error_msg, 'A user with that username already exists.')

    def test_weak_password(self):
        # Ok, now the email and the username are unique.
        # Password '1234' is too weak ?!! (Maybe)
        self.browser.get(self.url)
        self.compile_signup_form('test_test@mail.com', 'test_test', '1234')
        error_msg = self.browser.find_elements_by_class_name(
            'invalid-feedback')[1].text
        self.assertIn('This password is too common.', error_msg)

    def test_valid_form_compilation(self):
        # Finally. He signup procedure is subimt! :)
        self.browser.get(self.url)
        self.compile_signup_form('test_test@mail.com', 'test_test', 'md934y91us1')
        self.assertEqual(
            self.browser.current_url, f'{self.live_server_url}/login/')
        # He see a message: "conferm your email".
        msg = self.browser.find_element_by_xpath(
            '//div[@class="alert alert-success"]').text
        self.assertIn('An email was set to your address', msg)


# Now just a final step: he have to conferm his email in order to complete
# the registration process.

class EmailConfermationTest(StaticLiveServerTestCaseSelenium):

    # # Here is not used the fixtures beacuse the user in fixtures is
    # # a verifided one.

    def test_invalid_email_confermation(self):
        # He forget to conferm his email so he can't access to the dashboard
        self.browser.get(f'{self.live_server_url}/signup/')
        self.compile_signup_form('test1@mail.com', 'test1', 'md934y91us1')
        self.compile_login_form('test_test', 'md934y91us1')
        msg = self.browser.find_element_by_xpath(
            '//div[@class="alert alert-danger mt-4"]').text
        self.assertEqual(msg, 'Incorrect username and password.')

    def test_valid_email_confermation(self):
        # Now he caw he can to login into dashboard and use other aao features
        # like the REST-API and the python wrapper
        self.browser.get(f'{self.live_server_url}/signup/')
        self.compile_signup_form('test2@mail.com', 'test2', 'md934y91us1')
        verification_link = self.get_verification_link('test2@mail.com')
        self.browser.get(verification_link)
        # Now he know that his account is verified
        msg = self.browser.find_element_by_xpath(
            '//div[@class="alert alert-success"]').text
        self.assertEqual('Your account is now activated.', msg)
        self.compile_login_form('test2', 'md934y91us1')
        self.assertEqual(
            self.browser.current_url, f'{self.live_server_url}/dashboard/')


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
