from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse

from .models import Recipe

# Create your views here.
def home(request):
    recipes = Recipe.objects.all()
    return render(request, 'home.html', {'recipes':recipes})


def create_recipe(request):
    if request.method == 'POST':
        recipe = Recipe.objects.create(title=request.POST.get('recipe_title', ''))
        return redirect(reverse('show_recipe', args=[recipe.id]))

    return render(request, 'create_recipe.html', {'form':None})


def show_recipe(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    return render(request, 'show_recipe.html', {'recipe_title':recipe.title})
