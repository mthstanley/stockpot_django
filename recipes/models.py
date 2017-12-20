from django.db import models

from users.models import Profile

# Create your models here.
class Recipe(models.Model):
    title = models.TextField(default='')
    author = models.ForeignKey(Profile, related_name='recipes', null=True)


class RecipeStep(models.Model):
    body = models.TextField(default='')
    recipe = models.ForeignKey(Recipe, related_name='steps', null=True)
