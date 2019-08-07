from django.test import TestCase
from django.urls import resolve

from home.views import HomePageView


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_viwes(self):
        found = resolve('/')
        self.assertEqual(found.func.__name__, HomePageView.as_view().__name__)

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home/home_page.html')
