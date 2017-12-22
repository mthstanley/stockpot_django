from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory

from .models import Recipe, RecipeStep
from .forms import RecipeForm

# Create your views here.
def home(request):
    recipes = Recipe.objects.all()
    return render(request, 'home.html', {'recipes':recipes})

@login_required
def create_recipe(request):
    StepFormSet = inlineformset_factory(Recipe, RecipeStep, fields=('body',),
            extra=1, can_delete=False)
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        form.stepsformset = StepFormSet(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user.profile
            recipe.save()
            if form.stepsformset.is_valid():
                form.stepsformset.instance = recipe
                form.stepsformset.save()
            return redirect('show_recipe', pk=recipe.pk)
    else:
        form = RecipeForm()
        form.stepsformset = StepFormSet()

    return render(request, 'create_recipe.html', {'form':form})

@login_required
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.author.user != request.user:
        raise PermissionDenied

    StepFormSet = inlineformset_factory(Recipe, RecipeStep, fields=('body',),
            extra=1, can_delete=False)

    form = RecipeForm(request.POST or None, instance=recipe)
    form.stepsformset = StepFormSet(request.POST or None, request.FILES or None,
            instance=recipe)
    if form.is_valid():
        form.save()
        if form.stepsformset.is_valid():
            form.stepsformset.save()
        return redirect('show_recipe', pk=recipe.pk)
    return render(request, 'edit_recipe.html', {'form':form})

@login_required
def remove_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.author.user != request.user:
        raise PermissionDenied

    recipe.delete()
    return redirect('home')

def show_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'show_recipe.html', {'recipe':recipe})
