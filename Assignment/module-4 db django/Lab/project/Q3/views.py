from django.shortcuts import render


def home(request):
    """Render a form page with client-side (JavaScript) validation."""

    # On successful POST (valid server-side), you could process data here.
    # For this demo, we always render the same template and rely on JS for client-side validation.
    return render(request, 'Q3/form.html', {
        'title': 'Q3 - JS Form Validation',
    })
