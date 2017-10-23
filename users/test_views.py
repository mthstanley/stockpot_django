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
        user = User.objects.create_user(**self.credentials)
        self.client.login(**self.credentials)
        response = self.client.get(reverse('show_profile', args=[user.username]))
        self.assertIsNotNone(response.context['display_user'])
        self.assertTemplateUsed(response, 'show_profile.html')


class UserProfileEditViewTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'test',
            'email': 'test@example.com',
            'password': 'p@33w0rd',
        }

        self.user = User.objects.create_user(**self.credentials)

    def test_user_edit_profile_view_exists(self):
        self.client.login(**self.credentials)
        response = self.client.get(reverse('edit_profile', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)

    def test_profile_updates_persist(self):
        self.client.login(**self.credentials)
        name = 'Monty Python'
        bio = 'Software developer and food nerd.'
        self.assertEqual(self.user.profile.name, '')
        self.assertEqual(self.user.profile.bio, '')
        response = self.client.post(reverse('edit_profile', args=[self.user.username]),
                data={'name':name, 'bio':bio}, follow=True)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.name, name)
        self.assertEqual(self.user.profile.bio, bio)

    def test_login_required_to_edit_profile(self):
        name = 'Monty Python'
        edit_profile_url = reverse('edit_profile', args=[self.user.username])
        response = self.client.post(edit_profile_url, data={'name':name},
                follow=True)
        self.user.profile.refresh_from_db()
        login_url = reverse('login')
        self.assertRedirects(response, f'{login_url}?next={edit_profile_url}')
        self.assertEquals(self.user.profile.name, '')

    def test_can_only_edit_own_profile(self):
        wrong_user = {
            'username':'wrong',
            'email':'wrong@user.com',
            'password':'firstnamelastinitialbirthday'
        }
        User.objects.create_user(**wrong_user)
        self.client.login(**wrong_user)
        name = 'Monty Python'
        edit_profile_url = reverse('edit_profile', args=[self.user.username])
        response = self.client.post(edit_profile_url, data={'name':name},
                follow=True)
        self.assertEqual(response.status_code, 403)
        self.user.profile.refresh_from_db()
        self.assertEquals(self.user.profile.name, '')

    def test_instatiates_form_with_profile_attributes(self):
        name = 'Monty Python'
        bio = 'Software developer and food nerd.'
        self.user.profile.name = name
        self.user.profile.bio = bio
        self.user.profile.save()
        self.client.login(**self.credentials)
        response = self.client.get(reverse('edit_profile', args=[self.user.username]))
        form = response.context['form']
        self.assertEqual(form.initial['name'], self.user.profile.name)
        self.assertEqual(form.initial['bio'], self.user.profile.bio)
