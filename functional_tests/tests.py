from django.test import LiveServerTestCase
from django.contrib import auth
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.credentials = {
                    'username':'julia',
                    'email': 'julia@example.com',
                    'password': 'julia'
                }
        self.test_user = auth.models.User.objects.create_user(**self.credentials)

    def tearDown(self):
        self.browser.quit()

    def test_can_visit_website(self):

        # Monty wants a website where he can store his recipes, he has heard
        # about stockpot and decides to try it out
        self.browser.get(self.live_server_url)

        # he notices that the root url is always /recipes/
        self.assertIn('/recipes/', self.browser.current_url)

        # he notices Recipes in the title
        self.assertIn('Recipes', self.browser.title)

        # the header of the page welcomes him as a stranger
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Welcome, Stranger!', header_text)

    def test_can_login(self):

        # Julia wants a website where she can store her recipes, she has heard
        # about stockpot and decides to try it out
        self.browser.get(self.live_server_url)

        # she sees a link to login which she clicks
        login_link = self.browser.find_element_by_id('login')
        login_link.click()

        # she is redirected to login page
        self.assertIn('/accounts/login/', self.browser.current_url)

        # she writes her username and password and clicks login
        username_input = self.browser.find_element_by_id('id_username')
        password_input = self.browser.find_element_by_id('id_password')
        login_submit = self.browser.find_element_by_css_selector('input[type="submit"]')

        username_input.send_keys('julia')
        password_input.send_keys('julia') # silly julia that's a terrible password
        login_submit.click()

        # she sees that now the webpage welcomes her
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Welcome, julia!', header_text)



