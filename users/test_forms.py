from django.test import TestCase
from django.contrib.auth.models import User

from .forms import ProfileForm


class ProfileFormTest(TestCase):


    def setUp(self):
        self.credentials = {
                    'username':'username',
                    'email': 'email@example.com',
                    'password': 'password',
                }
        self.test_user = User.objects.create_user(**self.credentials)

    def test_valid_entry(self):
        form = ProfileForm({
            'name': 'Monty Python',
            'bio': 'Software developer and food nerd.'
        },
        instance=self.test_user.profile)
        self.assertTrue(form.is_valid())
        user_profile = form.save()
        self.assertEqual(user_profile.name, 'Monty Python')
        self.assertEqual(user_profile.bio, 'Software developer and food nerd.')

    def test_blank_optional_fields(self):
        form = ProfileForm({
            'name': '',
            'bio': ''
        },
        instance=self.test_user.profile)
        self.assertIsNone(form.fields['bio'].initial)
        self.assertIsNone(form.fields['name'].initial)
        self.assertTrue(form.is_valid())
        user_profile = form.save()
        self.assertEqual(user_profile.bio, '')
        self.assertEqual(user_profile.name, '')
