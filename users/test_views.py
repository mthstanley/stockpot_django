from django.test import TestCase
from django.core.urlresolvers import resolve, reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile

# Create your tests here.
class RegisterViewsTests(TestCase):

    def setUp(self):
        self.credentials = {
                    'username':'register',
                    'email': 'register@test.com',
                    'password1': 'p@33w0rd',
                    'password2': 'p@33w0rd',
        }

    def test_uses_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_uses_correct_form(self):
        response = self.client.get(reverse('register'))
        self.assertIsInstance(response.context['form'], UserCreationForm)

    def test_user_can_register(self):
        response = self.client.post(reverse('register'),
                self.credentials, follow=True)
        self.assertIsNotNone(User.objects.get(username=self.credentials['username']))

    def test_invalid_register_form(self):
        response = self.client.post(reverse('register'), {}, follow=True)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        # check the database
        # should be no users
        self.assertEqual(User.objects.count(), 0)
        # make sure we're still on the register page
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_register_redirect(self):
        # after successfully registering, the user should be redirected
        # to the home page
        response = self.client.post(reverse('register'),
                self.credentials, follow=True)
        self.assertRedirects(response, expected_url=reverse('home'),
                status_code=302, target_status_code=200)


class UserProfileViewTests(TestCase):

    def setUp(self):
        self.register_credentials = {
                    'username':'register',
                    'email': 'register@test.com',
                    'password1': 'p@33w0rd',
                    'password2': 'p@33w0rd',
        }

        self.credentials = {
            'username': 'test',
            'email': 'test@example.com',
            'password': 'p@33w0rd',
        }

    def test_user_signup_creates_user_profile(self):
        response = self.client.post(reverse('register'),
                self.register_credentials, follow=True)
        user = User.objects.get(username=self.register_credentials['username'])
        self.assertTrue(isinstance(user.profile, Profile))

    def test_user_profile_view_exists(self):
        user = User.objects.create(**self.credentials)
        self.client.login(**self.credentials)
        response = self.client.get(reverse('show_profile', args=[user.username]))
        self.assertIsNotNone(response.context['display_user'])
        self.assertTemplateUsed(response, 'show_profile.html')
