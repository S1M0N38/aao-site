import os
import re

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import mail

from selenium import webdriver

# # Just a python files contains some function used multiple times in
# # functional tests


class StaticLiveServerTestCaseSelenium(StaticLiveServerTestCase):

    fixtures = ['users']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Chrome()
        cls.browser.set_window_size(1280, 720)
        cls.browser.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def compile_signup_form(self, email, username, password):
        email_box = self.browser.find_element_by_name('email')
        username_box = self.browser.find_element_by_name('username')
        password_box = self.browser.find_element_by_name('password1')
        email_box.send_keys(email)
        username_box.send_keys(username)
        password_box.send_keys(password)
        self.browser.find_element_by_name('submit').click()

    def compile_login_form(self, username, password):
        username_box = self.browser.find_element_by_name('username')
        password_box = self.browser.find_element_by_name('password')
        username_box.send_keys(username)
        password_box.send_keys(password)
        self.browser.find_element_by_name('submit').click()

    def get_verification_link(self, email):
        return re.findall('href="([^"]*)"', mail.outbox[0].body)[0]
