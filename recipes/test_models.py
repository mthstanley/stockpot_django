from django.test import TestCase

from .models import Recipe, RecipeStep, Ingredient, MeasuredIngredient


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

    def test_add_steps_to_recipe(self):
        recipe = Recipe.objects.create(title='Grilled Cheese')

        step1 = RecipeStep.objects.create(body='Put cheese between two slices of bread.')
        step2 = RecipeStep.objects.create(body='Butter outside of sandwich.')
        step3 = RecipeStep.objects.create(body='Grill sandwich.')

        recipe.steps.add(step1, step2, step3)
        recipe.save()

        self.assertEqual(step1.body, recipe.steps.all()[0].body)
        self.assertEqual(recipe.steps.count(), 3)

    def test_delete_steps_on_recipe_delete(self):
        recipe = Recipe.objects.create(title='Grilled Cheese')

        step1 = RecipeStep.objects.create(body='Put cheese between two slices of bread.')
        step2 = RecipeStep.objects.create(body='Butter outside of sandwich.')
        step3 = RecipeStep.objects.create(body='Grill sandwich.')

        recipe.steps.add(step1, step2, step3)
        recipe.save()

        self.assertEqual(RecipeStep.objects.count(), 3)
        recipe.delete()
        self.assertEqual(RecipeStep.objects.count(), 0)

    def test_add_ingredients_to_recipe(self):
        recipe = Recipe.objects.create(title="Grilled Cheese")

        ing1 = Ingredient.objects.create(name='cheese')
        ing2 = Ingredient.objects.create(name='bread')
        ing3 = Ingredient.objects.create(name='butter')

        mi1 = MeasuredIngredient.objects.create(recipe=recipe, ingredient=ing1)
        mi2 = MeasuredIngredient.objects.create(recipe=recipe, ingredient=ing2)
        mi3 = MeasuredIngredient.objects.create(recipe=recipe, ingredient=ing3)

        self.assertEqual(recipe.ingredients.count(), 3)
        self.assertIn('cheese', [ing.name for ing in recipe.ingredients.all()])

    def test_keep_ingredients_on_delete_recipe(self):
        recipe = Recipe.objects.create(title="Grilled Cheese")

        ing1 = Ingredient.objects.create(name='cheese')
        ing2 = Ingredient.objects.create(name='bread')
        ing3 = Ingredient.objects.create(name='butter')

        mi1 = MeasuredIngredient.objects.create(recipe=recipe, ingredient=ing1)
        mi2 = MeasuredIngredient.objects.create(recipe=recipe, ingredient=ing2)
        mi3 = MeasuredIngredient.objects.create(recipe=recipe, ingredient=ing3)

        recipe.delete()
        self.assertEqual(MeasuredIngredient.objects.count(), 0)
        self.assertEqual(Ingredient.objects.count(), 3)
        self.assertEqual(Recipe.objects.count(), 0)

    def delete_ingredient_from_all_recipes(self):
        recipe1 = Recipe.objects.create(title="Grilled Cheese")
        recipe2 = Recipe.objects.create(title="Cheddar Soup")

        ing1 = Ingredient.objects.create(name='cheese')
        ing2 = Ingredient.objects.create(name='butter')

        mi1 = MeasuredIngredient.objects.create(recipe=recipe1, ingredient=ing1)
        mi2 = MeasuredIngredient.objects.create(recipe=recipe1, ingredient=ing2)
        mi3 = MeasuredIngredient.objects.create(recipe=recipe2, ingredient=ing1)

        ing1.delete()
        self.assertEqual(MeasuredIngredient.objects.count(), 1)
        self.assertEqual(recipe2.ingredients.count(), 0)
        self.assertEqual(recipe1.ingredients.count(), 1)
