from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('q13_login')
    else:
        form = UserCreationForm()
    return render(request, 'Q13/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            return redirect('q13_profile')
    else:
        form = AuthenticationForm()
    return render(request, 'Q13/login.html', {'form': form})


@login_required(login_url='q13_login')
def profile(request):
    return render(request, 'Q13/profile.html', {'user': request.user})


def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('q13_login')
