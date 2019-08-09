from django.contrib.staticfiles.testing import StaticLiveServerTestCase
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