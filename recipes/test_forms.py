from django.test import TestCase
from django.forms import inlineformset_factory
from django.forms.models import model_to_dict

from .forms import RecipeForm, MeasuredIngredientForm
from .models import Recipe, MeasuredIngredient, Ingredient, RecipeStep


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


class MeasuredIngredientFormTest(TestCase):


    def test_valid_data(self):
        recipe = Recipe.objects.create(title='Mashed Potatoes')
        form = MeasuredIngredientForm({
            'recipe': recipe.id,
            'amount': 1.5,
            'units': 'c',
            'ingredient': 'potato'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        recipe = Recipe.objects.create(title='Mashed Potatoes')
        form = MeasuredIngredientForm({
            'recipe': recipe.id,
            'amount': 'string',
            'units': 'c',
        })
        self.assertEqual(form.errors.as_data()['amount'][0].code, 'invalid')
        self.assertEqual(form.errors.as_data()['ingredient'][0].code, 'required')
        self.assertFalse(form.is_valid())

    def test_creates_new_ingredient_on_save(self):
        recipe = Recipe.objects.create(title='Mashed Potatoes')
        form = MeasuredIngredientForm({
            'recipe': recipe.id,
            'amount': 1.5,
            'units': 'c',
            'ingredient': 'potato'
        })
        self.assertEqual(Ingredient.objects.count(), 0)
        form.is_valid()
        form.save()
        self.assertEqual(Ingredient.objects.count(), 1)

    def test_uses_existing_ingredient(self):
        recipe = Recipe.objects.create(title='Mashed Potatoes')
        ingredient = Ingredient.objects.create(name='potato')
        form = MeasuredIngredientForm({
            'recipe': recipe.id,
            'amount': 1.5,
            'units': 'c',
            'ingredient': 'potato'
        })
        self.assertEqual(Ingredient.objects.count(), 1)
        form.is_valid()
        form.save()
        self.assertEqual(Ingredient.objects.count(), 1)

    def test_ingredient_name_value_case_insensitive(self):
        recipe = Recipe.objects.create(title='Mashed Potatoes')
        ingredient = Ingredient.objects.create(name='potato')
        form = MeasuredIngredientForm({
            'recipe': recipe.id,
            'amount': 1.5,
            'units': 'c',
            'ingredient': 'POTATO'
        })
        self.assertEqual(Ingredient.objects.count(), 1)
        form.is_valid()
        form.save()
        self.assertEqual(Ingredient.objects.count(), 1)

    def test_edit_existing_measuredingredient(self):
        recipe = Recipe.objects.create(title='Mashed Potatoes')
        ingredient = Ingredient.objects.create(name='potato')
        mi = MeasuredIngredient.objects.create(recipe=recipe, ingredient=ingredient,
                amount=1.5, units='c')
        self.assertEqual(Ingredient.objects.count(), 1)
        data = model_to_dict(mi)
        data.update({'ingredient': 'butter'})
        form = MeasuredIngredientForm(data=data, instance=mi)
        self.assertTrue(form.is_valid())
        form.save()
        # still only have one MeasuredIngredient object
        self.assertEqual(MeasuredIngredient.objects.count(), 1)
        # 2 Ingredient objects, butter and potato
        self.assertEqual(Ingredient.objects.count(), 2)
        # the MeasureIngredient object's ingredient name is now butter
        # instead of potato
        self.assertEqual(mi.ingredient.name, 'butter')
