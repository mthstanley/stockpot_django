from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth import get_user
from django.contrib.auth.models import User


from recipes.views import home


class HomePageTest(TestCase):


    def test_uses_correct_root_url(self):
        response = self.client.get('/')
        # test permanent url redirection code==301
        self.assertRedirects(response, expected_url=reverse('home'), status_code=301, target_status_code=200)

    def test_uses_home_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')


class LoginTests(TestCase):

    def setUp(self):
        self.credentials = {
                    'username':'username',
                    'email': 'email@example.com',
                    'password': 'password',
                }
        self.test_user = User.objects.create_user(**self.credentials)


    def test_login_urls_setup(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_user_can_login(self):
        # should be AnonymousUser which is not authenticated
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated())

        response = self.client.post(reverse('login'), self.credentials, follow=True)

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated())

    def test_user_can_logout(self):
        self.client.login(**self.credentials)

        self.client.get(reverse('logout'))

        # should be AnonymousUser which is not authenticated
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated())

    def test_uses_logout_template(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/logged_out.html')
