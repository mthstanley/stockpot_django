from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest


from recipes.views import home


class HomePageTest(TestCase):


    def test_uses_correct_root_url(self):
        response = self.client.get('/')
        self.assertEqual(response['location'], '/recipes/')

    def test_uses_home_template(self):
        response = self.client.get('/recipes/')
        self.assertTemplateUsed(response, 'home.html')


class LoginTests(TestCase):


    def test_login_urls_setup(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
