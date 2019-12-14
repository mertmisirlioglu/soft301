from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render

from website.models import Event, Ticket, UserProfile
from .forms import UserReg, ExtendedUserCreationForm, BuyTicketForm


def home(request):
    event_list = Event.objects.all()
    context = {"event_list": event_list}
    return render(request, 'home.html', context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is not correct!')
            return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html',
                      {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def signup(request):
    form = ExtendedUserCreationForm(request.POST or None)
    profile_form = UserReg(request.POST or None)
    print(form.errors)
    if form.is_valid() and profile_form.is_valid():
        user = form.save()
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'registration/signup.html',
                  {'form': ExtendedUserCreationForm, 'profile_form': UserReg})


def event_preview(request, pk):
    event = get_object_or_404(Event, pk=pk)
    context = {"event": event}
    return render(request, 'event/event_review.html', context)


@login_required
def ticket_buy_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        user = request.user
        form = BuyTicketForm(request.POST)
        if form.is_valid():
            print('mert')

            quantity = form.cleaned_data.get('quantity')

            for i in range(0, int(quantity)):
                ticket = Ticket(event=event, user=user)
                ticket.save()

            return redirect('home')
    else:
        form = BuyTicketForm()

    context = {'event': event, 'form': form}
    return render(request, 'ticket/buyTicketPage.html', context)


@login_required
def my_tickets_view(request):
    user = request.user
    ticket_list = Ticket.objects.all().filter(user=user)
    context = {"ticket_list": ticket_list}
    return render(request, 'profile/my_tickets.html', context)


@login_required
def my_profile_view(request):
    user = request.user
    user_infos = UserProfile.objects.all().filter(user=user)
    context = {"user_infos": user_infos}
    return render(request, 'profile/profile.html', context)
