from django import forms
from django.forms.widgets import TextInput

from .models import Recipe, MeasuredIngredient, Ingredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title',)


class MeasuredIngredientForm(forms.ModelForm):
    class Meta:
        model = MeasuredIngredient
        fields = ('recipe', 'amount', 'units', 'ingredient')

    # overide default Foreign Key field for ingredient to be a char field
    # this will take the name of the ingredient, which will be changed
    # to and ingredient object in the clean method
    ingredient = forms.CharField(label='Name', max_length=128)

    def __init__(self, *args, **kwargs):
        super(MeasuredIngredientForm, self).__init__(*args, **kwargs)

        _ingredient_pk = self.initial.get('ingredient', None)
        if _ingredient_pk:
            self.initial['ingredient'] = Ingredient.objects.get(pk=_ingredient_pk).name

    def clean(self):
        self.cleaned_data = super(MeasuredIngredientForm, self).clean()

        name = self.cleaned_data.get('ingredient')
        if name is not None:
            # see if the name given for an ingredient exists, if it
            # does use that ingredient
            ing = Ingredient.objects.filter(name=name.lower()).first()
            if ing is None:
                # if it doesn't exist, create the ingredient (lowercase)
                #TODO: find a better way to force lowercase in database
                ing = Ingredient.objects.create(name=name.lower())

            self.cleaned_data['ingredient'] = ing

        return self.cleaned_data
