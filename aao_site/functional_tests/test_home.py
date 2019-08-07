from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


# Bob is simple person, he land on the home page and just take a look at that;
# he just want to know what Against All Odds is about.

class HomePageTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Chrome()
        cls.browser.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_against_all_odds_in_title(self):
        # - Where am I? - said Bob. Ahhh, alright Against All Odds.
        self.browser.get(f'{self.live_server_url}/')
        self.assertEqual(self.browser.title, 'Against All Odds')
        # But wait, what is exactly Against All Odds?

    def test_button_python_disabled(self):
        # He start to click every where in order to understand more
        # The "python button" is disabled, maybe the python implemantation of
        # aao is not ready yet.
        self.browser.get(f'{self.live_server_url}/')
        button = self.browser.find_element_by_id('python')
        with self.assertRaises(WebDriverException):
            button.click()

    def test_button_dashboard_disabled(self):
        # Then he try to click on the "dashboard button" but also this button
        # seams to be disabled.
        self.browser.get(f'{self.live_server_url}/')
        button = self.browser.find_element_by_id('dashboard')
        with self.assertRaises(WebDriverException):
            button.click()

    def test_button_api_enable(self):
        # He doesn't give up and try to click on "API button" and this time
        # he is redirected to an external website: the aao REST-API docs!
        self.browser.get(f'{self.live_server_url}/')
        button = self.browser.find_element_by_id('api')
        button.click()
        docs_url = 'https://s1m0n38.github.io/aao-site-docs/'
        self.assertEqual(self.browser.current_url, docs_url)
