from django.shortcuts import render


def home_menu(request):
    """Render the Grand Line Projects - One Piece themed home menu page."""
    return render(request, 'home/index.html')
