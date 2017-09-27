from django.db import models

# Create your models here.
class Recipe(models.Model):
    title = models.TextField(default='')
