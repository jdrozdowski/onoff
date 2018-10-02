from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EditProfileForm, EditUserForm, RegistrationForm, ReportUserForm, UserProfileForm
from .models import UserProfile


def register(request):
    if request.user.is_authenticated:
        return redirect('events:mine')

    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = new_user
            profile.save()

            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('events:index')

    else:
        user_form = RegistrationForm(label_suffix='')
        profile_form = UserProfileForm(label_suffix='')

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'registration/register.html', context)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Zmiany zostały pomyślnie zapisane.')
            return redirect('profile', username=request.user.username)

    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'registration/edit.html', context)


@login_required
def profile(request, username):
    profile = get_object_or_404(UserProfile, user__username=username)

    storage = messages.get_messages(request)

    context = {
        'profile': profile,
        'messages': storage
    }

    return render(request, 'profiles/detail.html', context)


@login_required
def report(request, username):
    get_object_or_404(UserProfile, user__username=username)

    if username == request.user.username:
        return redirect('profile', username=username)

    if request.method == 'POST':
        form = ReportUserForm(request.POST)

        if form.is_valid():
            new_violation = form.save(commit=False)
            new_violation.sender = request.user
            new_violation.reported_user = User.objects.get(username=username)

            new_violation.save()

            messages.success(request, 'Zgłoszenie zostało pomyślnie przesłane. Dziękujemy.')
            return redirect('profile', username=username)

    else:
        form = ReportUserForm(label_suffix='')

    context = {
        'username': username,
        'form': form
    }

    return render(request, 'profiles/report.html', context)
