from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from recipes.models import Recipe, RecipeStep, Ingredient, MeasuredIngredient

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.julia_credentials = {
                    'username':'julia',
                    'email': 'julia@example.com',
                    'password': 'julia'
                }
        self.henry_credentials = {
                    'username':'henry',
                    'email': 'henry@example.com',
                    'password': 'henry'
                }
        self.user_henry = User.objects.create_user(**self.henry_credentials)


    def tearDown(self):
        self.browser.quit()
        User.objects.all().delete()

    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)


    def login_user(self, username, password):
        self.client.login(username=username, password=password)
        cookie = self.client.cookies['sessionid']
        self.browser.get(self.live_server_url)
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.browser.refresh() #need to update page for logged in user
        self.browser.get(self.live_server_url)

    def is_element_present(self, finder, locator):
        try:
            finder(locator)
        except NoSuchElementException:
            return False
        return True

    def fill_out_step(self, pk, text):
        step_textarea = self.browser.find_element_by_id(f'id_steps-{pk}-body')
        step_textarea.send_keys(text)

    def fill_out_ingredient(self, pk, amount, units, name):
        ingredient_amount_input = self.browser.find_element_by_id(f'id_measuredingredient_set-{pk}-amount')
        ingredient_amount_input.send_keys(str(amount))

        ingredient_units_input = self.browser.find_element_by_id(f'id_measuredingredient_set-{pk}-units')
        ingredient_units_input.send_keys(units)

        ingredient_ingredient_input = self.browser.find_element_by_id(f'id_measuredingredient_set-{pk}-ingredient')
        ingredient_ingredient_input.send_keys(name)

    def test_can_visit_website(self):

        # Monty wants a website where he can store his recipes, he has heard
        # about stockpot and decides to try it out
        self.browser.get(self.live_server_url)

        # he notices that the root url is always /recipes/
        self.assertIn(reverse('home'), self.browser.current_url)

        # he notices Recipes in the title
        self.assertIn('Recipes', self.browser.title)

        # the header of the page welcomes him as a stranger
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Welcome, Stranger!', header_text)

    def test_can_signup_login_logout(self):

        # Julia wants a website where she can store her recipes, she has heard
        # about stockpot and decides to try it out
        self.browser.get(self.live_server_url)

        # she sees a link to login which she clicks
        login_link = self.browser.find_element_by_id('login')
        login_link.click()

        # she is redirected to login page
        self.assertIn(reverse('login'), self.browser.current_url)

        # she is a new user and would like to register, so she clicks
        # the registration link
        register_link = self.browser.find_element_by_id('register')
        register_link.click()

        # she is taken to the registrations page
        self.assertIn(reverse('register'), self.browser.current_url)

        # she puts in a username, password and then verifies the password
        username_input = self.browser.find_element_by_id('id_username')
        password_input = self.browser.find_element_by_id('id_password1')
        verify_password_input = self.browser.find_element_by_id('id_password2')
        register_submit = self.browser.find_element_by_css_selector('input[type="submit"]')

        username_input.send_keys('julia')
        password_input.send_keys('p@33w0rd')
        verify_password_input.send_keys('p@33w0rd')
        register_submit.click()

        # she sees that now the webpage welcomes her
        self.wait_for(lambda: self.assertIn('Welcome, julia!',
            self.browser.find_element_by_tag_name('h1').text))

        # she is done viewing the website and would now like to logout
        # she sees the account toggle button and clicks it
        self.browser.find_element_by_css_selector('ul.navbar-right a.dropdown-toggle').click()
        # she sees the logout link and clicks it
        logout_link = self.browser.find_element_by_id('logout')
        logout_link.click()

        # she is told she successfully logged out and is welcomed to login again
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn("You've been successfully logged out", header_text)
        login_link = self.browser.find_element_by_id('login')

        # however she forgot to do something and wants to login again
        login_link.click()

        # she writes her username and password and clicks login
        username_input = self.browser.find_element_by_id('id_username')
        password_input = self.browser.find_element_by_id('id_password')
        login_submit = self.browser.find_element_by_css_selector('input[type="submit"]')

        username_input.send_keys('julia')
        password_input.send_keys('p@33w0rd') # silly julia that's a terrible password
        login_submit.click()

        # she is welcomed again by the web site
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Welcome, julia!', header_text)


    def test_can_create_recipe_and_view_later(self):
        self.browser.get(self.live_server_url)

        # after signing up for an account Henry would like to create a recipe
        # first he logs in
        self.login_user(self.henry_credentials['username'], self.henry_credentials['password'])

        # he then clicks on the account button to find the create new recipe button
        # in the dropdown menu
        self.browser.find_element_by_css_selector('ul.navbar-right a.dropdown-toggle').click()
        self.browser.find_element_by_id('create_recipe').click()

        # he is brought to a new page with a form for creating a recipe
        self.assertIn(reverse('create_recipe'), self.browser.current_url)

        # he fills out the recipe title in the form
        recipe_data = {
            'title': 'Tomato Soup',
            'step_body': 'Make the soup.',
            'ingredient_name': 'tomato puree',
            'ingredient_amount': 1.5,
            'ingredient_units': 'c'
        }
        title_input = self.browser.find_element_by_id('id_title')
        title_input.send_keys(recipe_data['title'])
        self.fill_out_step(0, recipe_data['step_body'])
        self.fill_out_ingredient(0, recipe_data['ingredient_amount'],
                recipe_data['ingredient_units'], recipe_data['ingredient_name'])
        self.browser.find_element_by_css_selector('button[type="submit"]').click()

        # when he hits submit he is redirected to the detail view of the recipe
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn(recipe_data['title'], header_text)
        steps = self.browser.find_elements_by_css_selector('li.step')
        self.assertIn(recipe_data['step_body'], [step.text for step in steps])
        ingredients = self.browser.find_elements_by_css_selector('li.ingredient')
        self.assertIn(str(recipe_data['ingredient_amount']), ingredients[0].text)
        self.assertIn(recipe_data['ingredient_units'], ingredients[0].text)
        self.assertIn(recipe_data['ingredient_name'], ingredients[0].text)

        # he then clicks the home link and find the list view of the recipe he created
        self.browser.find_element_by_link_text('Home').click()
        recipe_list = self.browser.find_element_by_id('id_recipe_list')
        recipes = recipe_list.find_elements_by_tag_name('li')
        self.assertIn(recipe_data['title'], [recipe.find_element_by_tag_name('h1').text for recipe in recipes])

        # he also notices that it also displays his username as the author of the recipe
        self.assertIn(self.henry_credentials['username'], recipes[0].find_element_by_tag_name('h2').text)

        # he then clicks the recipe title and is brought back to the recipe detail page
        created_recipe = Recipe.objects.get(title=recipe_data['title'])
        recipes[0].find_element_by_link_text(recipe_data['title']).click()
        self.assertIn(reverse('show_recipe', args=[created_recipe.pk]), self.browser.current_url)

    def test_user_profile_page(self):
        self.browser.get(self.live_server_url)

        # henry logs on and would like to view his profile page
        self.login_user(self.henry_credentials['username'], self.henry_credentials['password'])

        # he clicks on the profile link
        self.browser.find_element_by_link_text('Profile').click()
        self.assertIn(
                reverse('show_profile',
                    args=[self.henry_credentials['username']]),
                self.browser.current_url)

        # he sees his profile information
        username = self.browser.find_element_by_tag_name('h1')
        self.assertEquals(self.henry_credentials['username'], username.text)

    def test_can_edit_recipe(self):
        self.browser.get(self.live_server_url)

        ingredient = Ingredient.objects.create(name='tomato juice')
        step = RecipeStep.objects.create(body='Make the soup.')
        recipe = Recipe.objects.create(title='Tomato Soup', author=self.user_henry.profile)
        recipe.steps.add(step)
        recipe.save()
        mi = MeasuredIngredient.objects.create(recipe=recipe, ingredient=ingredient, amount=1, units='c')

        # henry would like to edit a recipe he previously created
        self.login_user(self.henry_credentials['username'], self.henry_credentials['password'])
        self.browser.find_element_by_link_text('Tomato Soup').click()

        # he sees and clicks the edit button on the recipes detail page
        self.browser.find_element_by_link_text('Edit').click()

        title_input = self.browser.find_element_by_id('id_title')
        step_textarea = self.browser.find_element_by_id('id_steps-0-body')

        # he sees that the input field are prepopulated
        self.assertEqual(step_textarea.get_attribute('value'), 'Make the soup.')
        ingredient_amount_input = self.browser.find_element_by_id('id_measuredingredient_set-0-amount')
        ingredient_units_input = self.browser.find_element_by_id('id_measuredingredient_set-0-units')
        ingredient_name_input = self.browser.find_element_by_id('id_measuredingredient_set-0-ingredient')
        self.assertEqual(ingredient_amount_input.get_attribute('value'), '1.000')
        self.assertEqual(ingredient_units_input.get_attribute('value'), 'c')
        self.assertEqual(ingredient_name_input.get_attribute('value'), 'tomato juice')
        # he deletes the text in the prepopulated title field
        title_input.clear()
        step_textarea.clear()
        ingredient_name_input.clear()
        title_input.send_keys('Tomato Bisque')
        step_textarea.send_keys('Eat the soup.')
        ingredient_name_input.send_keys('tomato puree')
        self.browser.find_element_by_css_selector('button[type=submit]').click()

        recipe.refresh_from_db()
        self.assertEqual(recipe.title, 'Tomato Bisque')
        self.assertEqual(recipe.steps.first().body, 'Eat the soup.')
        self.assertEqual(recipe.measuredingredient_set.first().ingredient.name, 'tomato puree')

    def test_can_delete_recipe(self):
        self.browser.get(self.live_server_url)

        recipe = Recipe(title='Tomato Soup', author=self.user_henry.profile)
        recipe.save()

        # henry would like to edit a recipe he previously created
        self.login_user(self.henry_credentials['username'], self.henry_credentials['password'])
        self.browser.find_element_by_link_text('Tomato Soup').click()

        # he sees and clicks the edit button on the recipes detail page
        self.browser.find_element_by_link_text('Remove').click()

        self.assertFalse(self.is_element_present(self.browser.find_element_by_link_text,
            'Tomato Soup'))
        self.assertEqual(Recipe.objects.count(), 0)

    def test_can_update_profile(self):
        self.browser.get(self.live_server_url)

        # henry would like to edit his profile page
        self.login_user(self.henry_credentials['username'], self.henry_credentials['password'])
        self.browser.find_element_by_link_text('Profile').click()

        self.browser.find_element_by_link_text('Edit').click()
        BIO = 'Food Scientist and Software Developer.'
        bio_input = self.browser.find_element_by_id('id_bio')
        bio_input.send_keys(BIO)

        self.browser.find_element_by_css_selector('button[type=submit]').click()

        self.assertIn(BIO, self.browser.page_source)

    def test_dynamic_formset_recipe_creation(self):
        self.browser.get(self.live_server_url)

        recipe = Recipe.objects.create(title='test recipe', author=self.user_henry.profile)
        step = RecipeStep.objects.create(body='step 1')
        ing = Ingredient.objects.create(name='potato')
        mi = MeasuredIngredient.objects.create(amount=1, units='c', ingredient=ing, recipe=recipe)
        recipe.steps.add(step)
        recipe.save()

        self.login_user(self.henry_credentials['username'], self.henry_credentials['password'])

        self.browser.get(self.live_server_url + reverse('edit_recipe', args=[recipe.pk]))

        WebDriverWait(self.browser, MAX_WAIT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.ingredient-formsets .add-row'))
        )

        ingredient_add_row = self.browser.find_element_by_css_selector('.ingredient-formsets .add-row')
        step_add_row = self.browser.find_element_by_css_selector('.step-formsets .add-row')

        self.fill_out_ingredient(1, 1.5, 'c', 'butter')
        self.fill_out_step(1, 'step 2')

        ingredient_add_row.click()
        self.fill_out_ingredient(2, 3, 'c', 'sugar')

        step_add_row.click()
        self.fill_out_step(2, 'step 3')

        self.browser.find_element_by_css_selector('button[type=submit]').click()

        recipe.refresh_from_db()
        self.assertEqual(recipe.steps.count(), 3)
        self.assertEqual(recipe.measuredingredient_set.count(), 3)

        self.browser.get(self.live_server_url + reverse('edit_recipe', args=[recipe.pk]))

        WebDriverWait(self.browser, MAX_WAIT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.ingredient-formsets .add-row'))
        )

        ingredient_formset = self.browser.find_element_by_css_selector('.ingredient-formsets p')
        ingredient_formset.find_element_by_css_selector('.delete-row').click()

        step_formset = self.browser.find_element_by_css_selector('.step-formsets p')
        step_formset.find_element_by_css_selector('.delete-row').click()

        self.browser.find_element_by_css_selector('button[type=submit]').click()

        recipe.refresh_from_db()
        self.assertEqual(recipe.steps.count(), 2)
        self.assertEqual(recipe.measuredingredient_set.count(), 2)
