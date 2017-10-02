from django.test import TestCase
from django.core.urlresolvers import resolve, reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile

# Create your tests here.
class RegisterTests(TestCase):

    def setUp(self):
        self.register_credentials = {
                    'username':'register',
                    'email': 'register@test.com',
                    'password1': 'p@33w0rd',
                    'password2': 'p@33w0rd',
        }


    def test_register_template_form(self):
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertIsInstance(response.context['form'], UserCreationForm)

    def test_user_can_register(self):
        response = self.client.post(reverse('register'), self.register_credentials, follow=True)
        self.assertIsNotNone(User.objects.get(username=self.register_credentials['username']))

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
        response = self.client.post(reverse('register'), self.register_credentials, follow=True)
        self.assertRedirects(response, expected_url=reverse('home'), status_code=302, target_status_code=200)


class UserProfileTests(TestCase):


    def setUp(self):
        self.register_credentials = {
                    'username':'register',
                    'email': 'register@test.com',
                    'password1': 'p@33w0rd',
                    'password2': 'p@33w0rd',
        }

    def test_user_signup_creates_user_profile(self):
        response = self.client.post(reverse('register'), self.register_credentials, follow=True)
        user = User.objects.get(username=self.register_credentials['username'])
        self.assertTrue(isinstance(user.profile, Profile))
