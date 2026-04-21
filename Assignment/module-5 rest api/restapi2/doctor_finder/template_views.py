"""
Template Views for the Doctor Finder app.
──────────────────────────────────────────────
Renders the HTML pages for the menu-based dashboard UI.
These are separate from the API views.
"""
from django.shortcuts import render
from .models import Doctor


def home_view(request):
    """Render the main dashboard / menu page."""
    stats = {
        'total_doctors': Doctor.objects.count(),
        'total_specialties': Doctor.objects.values_list('specialty', flat=True).distinct().count(),
    }
    return render(request, 'home.html', {'stats': stats})


def joke_page(request):
    """Page for the Random Joke feature."""
    return render(request, 'pages/joke.html')


def setup_page(request):
    """Page showing Django setup instructions."""
    return render(request, 'pages/setup.html')


def doctors_page(request):
    """Page for Doctor CRUD operations (interactive UI)."""
    doctors = Doctor.objects.all()
    return render(request, 'pages/doctors.html', {'doctors': doctors})


def auth_page(request):
    """Page for Token Authentication demo."""
    return render(request, 'pages/auth.html')


def weather_page(request):
    """Page for the Weather API feature."""
    return render(request, 'pages/weather.html')


def github_page(request):
    """Page for the GitHub API feature."""
    return render(request, 'pages/github.html')


def country_page(request):
    """Page for the Country Info feature."""
    return render(request, 'pages/country.html')




def otp_page(request):
    """Page for the OTP Verification feature."""
    return render(request, 'pages/otp.html')
