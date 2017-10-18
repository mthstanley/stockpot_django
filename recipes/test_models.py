from django.test import TestCase

from .models import Recipe


class RecipeModelTest(TestCase):


    def test_saving_and_retrieving_recipes(self):
        first_recipe_title = 'Tomato Soup'
        second_recipe_title = 'Grilled Cheese'

        first_recipe = Recipe()
        first_recipe.title = first_recipe_title
        first_recipe.save()

        second_recipe = Recipe()
        second_recipe.title = second_recipe_title
        second_recipe.save()

        saved_recipes = Recipe.objects.all()
        self.assertEqual(saved_recipes.count(), 2)

        first_saved_recipe = saved_recipes[0]
        second_saved_recipe = saved_recipes[1]
        self.assertEqual(first_saved_recipe.title, first_recipe_title)
        self.assertEqual(second_saved_recipe.title, second_recipe_title)
