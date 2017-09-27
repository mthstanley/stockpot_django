from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse

from .models import Recipe

# Create your views here.
def home(request):
    return render(request, 'home.html')


def create_recipe(request):
    if request.method == 'POST':
        recipe = Recipe()
        recipe.title = request.POST.get('recipe_title', '')
        recipe.save()

        return redirect(reverse('show_recipe', args=[recipe.id]))

    return render(request, 'create_recipe.html', {'form':None})


def show_recipe(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    return render(request, 'show_recipe.html', {'recipe_title':recipe.title})
