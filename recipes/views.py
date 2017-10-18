from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Recipe
from .forms import RecipeForm

# Create your views here.
def home(request):
    recipes = Recipe.objects.all()
    return render(request, 'home.html', {'recipes':recipes})

@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user.profile
            recipe.save()
            return redirect('show_recipe', pk=recipe.pk)
    else:
        form = RecipeForm()

    return render(request, 'create_recipe.html', {'form':form})

def show_recipe(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    return render(request, 'show_recipe.html', {'recipe':recipe})
