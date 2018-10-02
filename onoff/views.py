from django.shortcuts import redirect, render
from django.utils import timezone

from events.models import Event


def index(request):
    if request.user.is_authenticated:
        return redirect('events:mine')

    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:8]

    context = {
        'title': 'Spotkania',
        'events': events
    }

    context = {
        'title': 'Spotkania',
        'events': events
    }

    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


def bibliography(request):
    return render(request, 'bibliography.html')


def statute(request):
    return render(request, 'statute.html')
