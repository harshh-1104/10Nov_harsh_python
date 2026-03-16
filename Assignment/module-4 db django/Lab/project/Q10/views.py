from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # In a real app, you'd create the user here
            # For demo, just show success message
            messages.success(request, 'Registration successful!')
            return redirect('q10_register')
    else:
        form = RegistrationForm()
    return render(request, 'Q10/register.html', {'form': form})

