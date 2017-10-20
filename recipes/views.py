from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

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

@login_required
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.author.user != request.user:
        raise PermissionDenied

    form = RecipeForm(request.POST or None, instance=recipe)
    if form.is_valid():
        form.save()
        return redirect('show_recipe', pk=recipe.pk)
    return render(request, 'edit_recipe.html', {'form':form})

def show_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'show_recipe.html', {'recipe':recipe})
