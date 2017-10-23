from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied

from .forms import ProfileForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form':form})

def show_profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'show_profile.html', {'display_user':user})

@login_required
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    if user != request.user:
        raise PermissionDenied

    form = ProfileForm(request.POST or None, instance=user.profile)
    if form.is_valid():
        form.save()
        return redirect('show_profile', username=user.username)
    return render(request, 'edit_profile.html', {'form':form})
