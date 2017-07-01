from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

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
