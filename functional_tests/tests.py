from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse
from django.contrib import auth
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.credentials = {
                    'username':'julia',
                    'email': 'julia@example.com',
                    'password': 'julia'
                }

    def tearDown(self):
        self.browser.quit()

    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

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

