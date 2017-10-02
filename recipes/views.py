from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Recipe

# Create your views here.
def home(request):
    recipes = Recipe.objects.all()
    return render(request, 'home.html', {'recipes':recipes})

@login_required
def create_recipe(request):
    if request.method == 'POST':
        recipe = Recipe.objects.create(title=request.POST.get('recipe_title', ''), author=request.user.profile)
        return redirect(reverse('show_recipe', args=[recipe.id]))

    return render(request, 'create_recipe.html', {'form':None})

def show_recipe(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    return render(request, 'show_recipe.html', {'recipe':recipe})
