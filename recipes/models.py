from django.db import models

from users.models import Profile

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=128, default='')


class Recipe(models.Model):
    title = models.TextField(default='')
    author = models.ForeignKey(Profile, related_name='recipes', null=True)
    ingredients = models.ManyToManyField(Ingredient, through='MeasuredIngredient')


class RecipeStep(models.Model):
    body = models.TextField(default='')
    recipe = models.ForeignKey(Recipe, related_name='steps', null=True)


class MeasuredIngredient(models.Model):
    UNIT_CHOICES = (('c', 'cup'),)

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.DecimalField(default=0, max_digits=6, decimal_places=3)
    units = models.CharField(max_length=128, choices=UNIT_CHOICES, blank=True)
