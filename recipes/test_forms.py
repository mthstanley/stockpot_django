from django.test import TestCase

from .forms import RecipeForm


class RecipeFormTest(TestCase):


    def test_valid_data(self):
        form = RecipeForm({
            'title': 'Tomato Soup',
        })
        self.assertTrue(form.is_valid())
        recipe = form.save()
        self.assertEqual(recipe.title, 'Tomato Soup')

    def test_blank_data(self):
        form = RecipeForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'title': ['This field is required.'],
        })
