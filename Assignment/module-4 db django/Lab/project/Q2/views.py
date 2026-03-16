from django.shortcuts import render


def home(request):
    """Render a template that includes a static CSS stylesheet."""
    context = {
        'title': 'Q2 - Styled Template',
        'heading': 'Welcome to Q2',
        'subtitle': 'This page is styled using a CSS file in the Q2 app.',
    }
    return render(request, 'Q2/index.html', context)
