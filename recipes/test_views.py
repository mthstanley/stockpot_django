from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth import get_user
from django.contrib.auth.models import User


from .views import home
from .models import Recipe
from .forms import RecipeForm
from users.models import Profile


class HomeViewTest(TestCase):


    def test_uses_correct_root_url(self):
        response = self.client.get('/')
        # test permanent url redirection code==301
        self.assertRedirects(response, expected_url=reverse('home'),
                status_code=301, target_status_code=200)

    def test_uses_home_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_displays_all_list_items(self):
        Recipe.objects.create(title='Tomato Soup')
        Recipe.objects.create(title='Grilled Cheese')

        response = self.client.get(reverse('home'))

        self.assertIn('Tomato Soup', response.content.decode())
        self.assertIn('Grilled Cheese', response.content.decode())


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

        response = self.client.post(reverse('login'), self.credentials,
                follow=True)

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


class RecipeCrudTest(TestCase):


    def setUp(self):
        self.credentials = {
                    'username':'username',
                    'email': 'email@example.com',
                    'password': 'password',
                }
        self.test_user = User.objects.create_user(**self.credentials)

    def test_create_recipe_exists(self):
        # user must be logged in to create a recipe
        self.client.login(**self.credentials)
        response = self.client.get(reverse('create_recipe'))
        self.assertEqual(response.status_code, 200)

    def test_uses_create_recipe_template(self):
        self.client.login(**self.credentials)
        response = self.client.get(reverse('create_recipe'))
        self.assertTemplateUsed(response, 'create_recipe.html')

    def test_redirect_to_recipe_detail_view_on_create(self):
        self.client.login(**self.credentials)
        response = self.client.post(reverse('create_recipe'),
                data={'title': 'Tomato Soup'}, follow=True)
        recipe = Recipe.objects.get(title='Tomato Soup')
        self.assertRedirects(response, reverse('show_recipe', args=[recipe.pk]))
        self.assertIn('Tomato Soup', response.content.decode())
        self.assertTemplateUsed(response, 'show_recipe.html')

    def test_can_save_a_POST_request(self):
        self.client.login(**self.credentials)
        response = self.client.post(reverse('create_recipe'),
                data={'title': 'Tomato Soup'})

        self.assertEqual(Recipe.objects.count(), 1)
        new_recipe = Recipe.objects.first()
        self.assertEqual(new_recipe.title, 'Tomato Soup')

    def test_can_pass_new_recipe_id_to_show_recipe(self):
        new_recipe = Recipe()
        new_recipe.title = 'Tomato Soup'
        new_recipe.save()
        response = self.client.get(reverse('show_recipe', args=[new_recipe.pk]))
        self.assertIn('Tomato Soup', response.content.decode())

    def test_only_saves_recipes_when_necessary(self):
        self.client.login(**self.credentials)
        self.client.get(reverse('create_recipe'))
        self.assertEqual(Recipe.objects.count(), 0)

    def test_must_be_logged_in_to_create_recipe(self):
        response = self.client.post(reverse('create_recipe'),
                data={'title':'Tomato Soup'}, follow=True)
        login_url = reverse('login')
        create_recipe_url = reverse('create_recipe')
        self.assertRedirects(response, f'{login_url}?next={create_recipe_url}')
        self.assertEquals(Recipe.objects.count(), 0)

    def test_recipes_saves_author_on_create(self):
        self.client.login(**self.credentials)
        response = self.client.post(reverse('create_recipe'),
                data={'title': 'Tomato Soup'}, follow=True)
        recipe = Recipe.objects.get(title='Tomato Soup')
        self.assertIsNotNone(recipe.author)
        self.assertTrue(isinstance(recipe.author, Profile))

    def test_uses_recipe_form_on_create(self):
        self.client.login(**self.credentials)
        response = self.client.get(reverse('create_recipe'))
        self.assertIsInstance(response.context['form'], RecipeForm)
