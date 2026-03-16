from django.shortcuts import render


def home(request):
    """Render a simple template using Django's template engine."""
    context = {
        'title': 'Django Template Demo',
        'message': 'Hello from Django templates!',
    }
    return render(request, 'Q1/index.html', context)
