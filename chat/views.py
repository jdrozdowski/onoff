from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import MessageForm, MessageWithReceiverForm
from .models import Chat


@login_required
def index(request):
    chats = Chat.objects.filter(
        Q(participants=request.user) |
        Q(event__participants=request.user)
    )

    if chats:
        chat_ids = chats.exclude(message__isnull=True).values_list('pk', flat=True)

        if chat_ids:
            chat_id = chat_ids.latest('last_activity')

            return redirect('chat:detail', chat_id)

    return render(request, 'chat/index.html')


@login_required
def detail(request, chat_id):
    chat = get_object_or_404(Chat, pk=chat_id)

    if chat.participants and request.user not in chat.participants.all():
        if chat.event and request.user not in chat.event.participants.all():
            return redirect('chat:index')

    chats = Chat.objects.exclude(message__isnull=True).filter(
        Q(participants=request.user) |
        Q(event__participants=request.user)
    ).order_by('-last_activity')

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.chat = chat
            new_message.chat.last_activity = timezone.now()
            new_message.author = request.user

            new_message.chat.save()
            new_message.save()

            return redirect('chat:detail', chat_id=chat_id)

    else:
        form = MessageForm()

    context = {
        'chat': chat,
        'chats': chats,
        'form': form
    }

    return render(request, 'chat/detail.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = MessageWithReceiverForm(request.user, request.POST)

        if form.is_valid():
            receiver = form.cleaned_data['receiver'].get()

            chat, created = Chat.objects.filter(event__isnull=True, participants=request.user).filter(participants=receiver).get_or_create()

            if created:
                chat.participants.set([receiver, request.user])

            new_message = form.save(commit=False)
            new_message.chat = chat
            new_message.chat.last_activity = timezone.now()
            new_message.author = request.user

            new_message.chat.save()
            new_message.save()

            chat_id = chat.pk

            return redirect('chat:detail', chat_id=chat_id)

    else:
        form = MessageWithReceiverForm(request.user, initial={'receiver': request.GET.get('receiver', None)})

    context = {
        'form': form
    }

    return render(request, 'chat/create.html', context)
