from django.test import TestCase
from django.urls import reverse


class HomePageTest(TestCase):

    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_template_used(self):
        self.assertTemplateUsed(self.response, 'home/home_page.html')
