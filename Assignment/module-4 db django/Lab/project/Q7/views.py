from django.shortcuts import render, redirect
from .models import Message
from .forms import MessageForm

def message_list(request):
    """View (V) - Handles request logic and passes data to template."""
    messages = Message.objects.all().order_by('-created_at')
    return render(request, 'Q7/message_list.html', {
        'messages': messages,
        'title': 'Q7 - MVT Architecture Demo',
    })

def message_create(request):
    """View (V) - Processes form submission and interacts with model."""
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('q7_home')
    else:
        form = MessageForm()
    return render(request, 'Q7/message_form.html', {'form': form})

