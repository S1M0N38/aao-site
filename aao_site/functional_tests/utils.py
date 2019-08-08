from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

# # Just a python files contains some function used multiple times in
# # functional tests


class StaticLiveServerTestCaseSelenium(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Chrome()
        cls.browser.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()
