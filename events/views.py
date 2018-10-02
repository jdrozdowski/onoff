from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .forms import EventForm, PromoteToOrganizerForm, SearchEventForm
from .models import Event

from chat.forms import MessageForm
from chat.models import Chat

import datetime


def index(request):
    if request.GET.get('query') or request.GET.get('date') or request.GET.get('city'):
        form = SearchEventForm(request.GET, label_suffix='')

        if form.is_valid():
            query = form.cleaned_data['query']
            date = form.cleaned_data['date']
            city = form.cleaned_data['city']

            if date:
                if date < datetime.date.today():
                    return redirect(reverse('events:past') + '?query=%s&date=%s&city=%s' % (query, date, city))

                events_list = Event.objects.filter(date__contains=date).order_by('date')
            else:
                events_list = Event.objects.filter(date__gt=timezone.now()).order_by('date')

            if city:
                events_list = events_list.filter(city=city)

            if query:
                events_list = events_list.filter(
                    Q(title__icontains=query) |
                    Q(tags__name__icontains=query) |
                    Q(city__icontains=query) |
                    Q(city_area__icontains=query) |
                    Q(description__icontains=query)
                ).distinct()

        else:
            events_list = Event.objects.filter(date__gt=timezone.now()).order_by('date')

    else:
        form = SearchEventForm(request.GET, label_suffix='')

        events_list = Event.objects.filter(date__gt=timezone.now()).order_by('date')

        category = request.GET.get('category')
        tag = request.GET.get('tag')

        if tag:
            events_list = events_list.filter(tags__name=tag)

        if category:
            events_list = events_list.filter(category=category)

    paginator = Paginator(events_list, 8)
    page = request.GET.get('page')
    events = paginator.get_page(page)

    context = {
        'title': 'Spotkania',
        'events': events,
        'form': form
    }

    return render(request, 'events/index.html', context)


def past(request):
    if request.GET.get('query') or request.GET.get('date') or request.GET.get('city'):
        form = SearchEventForm(request.GET, label_suffix='')

        if form.is_valid():
            query = form.cleaned_data['query']
            date = form.cleaned_data['date']
            city = form.cleaned_data['city']

            if date:
                if date >= datetime.date.today():
                    return redirect(reverse('events:index') + '?query=%s&date=%s&city=%s' % (query, date, city))

                events_list = Event.objects.filter(date__contains=date).order_by('-date')
            else:
                events_list = Event.objects.filter(date__lte=timezone.now()).order_by('-date')

            if city:
                events_list = events_list.filter(city=city)

            if query:
                events_list = events_list.filter(
                    Q(title__icontains=query) |
                    Q(tags__name__icontains=query) |
                    Q(city__icontains=query) |
                    Q(city_area__icontains=query) |
                    Q(description__icontains=query)
                ).distinct()

        else:
            events_list = Event.objects.filter(date__lte=timezone.now()).order_by('-date')

    else:
        form = SearchEventForm(request.GET, label_suffix='')

        events_list = Event.objects.filter(date__lte=timezone.now()).order_by('-date')

        category = request.GET.get('category')

        if category:
            events_list = events_list.filter(category=category)

    paginator = Paginator(events_list, 8)
    page = request.GET.get('page')
    events = paginator.get_page(page)

    context = {
        'title': 'Spotkania',
        'events': events,
        'form': form
    }

    return render(request, 'events/past.html', context)


@login_required
def mine(request):
    if request.GET.get('query') or request.GET.get('date') or request.GET.get('city'):
        form = SearchEventForm(request.GET, label_suffix='')

        if form.is_valid():
            query = form.cleaned_data['query']
            date = form.cleaned_data['date']
            city = form.cleaned_data['city']

            if date:
                if date < datetime.date.today():
                    return redirect(reverse('events:mine_past') + '?query=%s&date=%s&city=%s' % (query, date, city))

                events_list = Event.objects.filter(participants=request.user).filter(date__contains=date).order_by('date')
            else:
                events_list = Event.objects.filter(participants=request.user).filter(date__gt=timezone.now()).order_by('date')

            if city:
                events_list = events_list.filter(city=city)

            if query:
                events_list = events_list.filter(
                    Q(title__icontains=query) |
                    Q(tags__name__icontains=query) |
                    Q(city__icontains=query) |
                    Q(city_area__icontains=query) |
                    Q(description__icontains=query)
                ).distinct()

        else:
            events_list = Event.objects.filter(participants=request.user).filter(date__gt=timezone.now()).order_by('date')

    else:
        form = SearchEventForm(request.GET, label_suffix='')

        events_list = Event.objects.filter(participants=request.user).filter(date__gt=timezone.now()).order_by('date')

        category = request.GET.get('category')

        if category:
            events_list = events_list.filter(category=category)

    paginator = Paginator(events_list, 8)
    page = request.GET.get('page')
    events = paginator.get_page(page)

    context = {
        'title': 'Spotkania',
        'events': events,
        'form': form
    }

    return render(request, 'events/mine.html', context)


@login_required
def mine_past(request):
    if request.GET.get('query') or request.GET.get('date') or request.GET.get('city'):
        form = SearchEventForm(request.GET, label_suffix='')

        if form.is_valid():
            query = form.cleaned_data['query']
            date = form.cleaned_data['date']
            city = form.cleaned_data['city']

            if date:
                if date >= datetime.date.today():
                    return redirect(reverse('events:mine') + '?query=%s&date=%s&city=%s' % (query, date, city))

                events_list = Event.objects.filter(participants=request.user).filter(date__contains=date).order_by('-date')
            else:
                events_list = Event.objects.filter(participants=request.user).filter(date__lte=timezone.now()).order_by('-date')

            if city:
                events_list = events_list.filter(city=city)

            if query:
                events_list = events_list.filter(
                    Q(title__icontains=query) |
                    Q(tags__name__icontains=query) |
                    Q(city__icontains=query) |
                    Q(city_area__icontains=query) |
                    Q(description__icontains=query)
                ).distinct()

        else:
            events_list = Event.objects.filter(participants=request.user).filter(date__lte=timezone.now()).order_by('-date')

    else:
        form = SearchEventForm(request.GET, label_suffix='')

        events_list = Event.objects.filter(participants=request.user).filter(date__lte=timezone.now()).order_by('-date')

        category = request.GET.get('category')

        if category:
            events_list = events_list.filter(category=category)

    paginator = Paginator(events_list, 8)
    page = request.GET.get('page')
    events = paginator.get_page(page)

    context = {
        'title': 'Spotkania',
        'events': events,
        'form': form
    }

    return render(request, 'events/mine.html', context)


def detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST' and request.user in event.participants.all():
        form = MessageForm(request.POST)

        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.chat = event.chat
            new_message.chat.last_activity = timezone.now()
            new_message.author = request.user

            new_message.chat.save()
            new_message.save()

            return redirect('events:detail', event_id=event_id)

    else:
        form = MessageForm()

    storage = messages.get_messages(request)

    context = {
        'event': event,
        'messages': storage,
        'form': form
    }

    return render(request, 'events/detail.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)

        if form.is_valid():
            new_event = form.save(commit=False)

            new_event.organizer = request.user
            new_event.date = form.cleaned_data['date']
            new_event.save()

            new_event.tags.set(form.cleaned_data['tags'])
            new_event.participants.add(request.user)

            Chat.objects.create(event=new_event)

            event_id = new_event.pk

            messages.success(request, 'Spotkanie zostało pomyślnie utworzone.')
            return redirect('events:detail', event_id=event_id)

    else:
        form = EventForm(label_suffix='')

    context = {
        'title': 'Stwórz nowe spotkanie',
        'form': form
    }

    return render(request, 'events/create.html', context)


@login_required
def edit(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.user != event.organizer:
        messages.error(request, 'Nie możesz edytować spotkania, którego nie jesteś organizatorem.')
        return redirect('events:detail', event_id=event_id)

    if event.is_expired:
        messages.error(request, 'Nie możesz edytować spotkania, które już się odbyło.')
        return redirect('events:detail', event_id=event_id)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)

        if form.is_valid():
            event = form.save(commit=False)

            event.date = form.cleaned_data['date']
            event.save()

            messages.success(request, 'Spotkanie zostało pomyślnie zmodyfikowane.')
            return redirect('events:detail', event_id=event_id)

    else:
        form = EventForm(instance=event, label_suffix='')

    context = {
        'title': 'Edytuj spotkanie',
        'form': form,
        'event_id': event_id
    }

    return render(request, 'events/edit.html', context)


@login_required
def delete(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.user != event.organizer:
        messages.error(request, 'Nie możesz usunąć spotkania, którego nie jesteś organizatorem.')
        return redirect('events:detail', event_id=event_id)

    if event.is_expired:
        messages.error(request, 'Nie możesz usunąć spotkania, które już się odbyło.')
        return redirect('events:detail', event_id=event_id)

    if request.method == 'POST':
        event.delete()

        messages.success(request, 'Spotkanie zostało pomyślnie usunięte.')
        return redirect('events:index')

    context = {
        'event': event
    }

    return render(request, 'events/delete.html', context)


@login_required
def join(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.user in event.participants.all():
        messages.error(request, 'Nie możesz dołączyć do spotkania, w którym już uczestniczysz.')
        return redirect('events:detail', event_id=event_id)

    if event.participants.count() == event.max_number_of_participants:
        messages.error(request, 'Brak wolnych miejsc. Nie możesz dołączyć do spotkania.')
        return redirect('events:detail', event_id=event_id)

    if event.is_expired:
        messages.error(request, 'Nie możesz dołączyć do spotkania, które już się odbyło.')
        return redirect('events:detail', event_id=event_id)

    event.participants.add(request.user)

    messages.success(request, 'Dołączyłeś do spotkania.')
    return redirect('events:detail', event_id=event_id)


@login_required
def leave(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.user not in event.participants.all():
        messages.error(request, 'Nie możesz opuścić spotkania, w którym nie uczestniczysz.')
        return redirect('events:detail', event_id=event_id)

    if event.is_expired:
        messages.error(request, 'Nie możesz opuścić spotkania, które już się odbyło.')
        return redirect('events:detail', event_id=event_id)

    if request.user == event.organizer:
        messages.error(request, 'Nie możesz opuścić spotkania, którego jesteś organizatorem. Aby móc opuścić spotkanie, przekaż rolę organizatora innemu uczestnikowi.')
        return redirect('events:detail', event_id=event_id)

    event.participants.remove(request.user)

    messages.success(request, 'Nie jesteś już uczestnikiem spotkania.')
    return redirect('events:detail', event_id=event_id)


@login_required
def promote_to_organizer(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.user != event.organizer:
        messages.error(request, 'Nie możesz przekazać roli organizatora, gdy nie jesteś organizatorem danego spotkania.')
        return redirect('events:detail', event_id=event_id)

    if event.is_expired:
        messages.error(request, 'Nie możesz przekazać roli organizatora w spotkaniu, które już się odbyło.')
        return redirect('events:detail', event_id=event_id)

    if event.participants.count() <= 1:
        messages.error(request, 'Nie możesz przekazać roli organizatora, ponieważ w spotkaniu nie uczestniczy nikt poza Tobą.')
        return redirect('events:detail', event_id=event_id)

    if request.method == 'POST':
        form = PromoteToOrganizerForm(request.POST, instance=event)

        if form.is_valid():
            event.save()

            messages.success(request, 'Organizator spotkania został pomyślnie zmieniony.')
            return redirect('events:detail', event_id=event_id)

    else:
        form = PromoteToOrganizerForm(instance=event)

    context = {
        'form': form
    }

    return render(request, 'events/promote_to_organizer.html', context)
