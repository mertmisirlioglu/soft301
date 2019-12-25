from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
import time
from django.contrib import messages

from website.models import Event, Ticket, UserProfile
from .forms import (UserReg,
                    ExtendedUserCreationForm,
                    BuyTicketForm,
                    EditProfileForm,
                    AddEvent,
                    PaymentForm)


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
    # profile_form.birthday = request.POST.get('birthday', '')
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
    else:
        return render(request, 'registration/signup.html',
                      {'form': ExtendedUserCreationForm, 'profile_form': UserReg})


def event_preview(request, pk):
    event = get_object_or_404(Event, pk=pk)
    context = {"event": event}
    return render(request, 'event/event_review.html', context)


def search_event(request):
    return render(request, 'event/searchPage.html')


@login_required
def ticket_buy_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        user = request.user
        user_infos = UserProfile.objects.get(user=user)
        form = BuyTicketForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data.get('quantity')
            quantity = int(quantity)
            if event.quota < quantity:
                messages.error(request, ("No quota available for buying "+ str(quantity)+" ticket"))
            elif user_infos.balance < event.price*quantity:
                messages.error(request, ("Your amount is not enough for buying " + str(quantity) + " ticket.\nYou need "+str(event.price*quantity-user_infos.balance)+"$ more."))

            else:
                user_infos.balance = user_infos.balance - event.price * quantity
                user_infos.save()
                event.quota -= quantity
                event.save()
                for i in range(0, int(quantity)):
                    ticket = Ticket(event=event, user=user)
                    ticket.save()

                messages.success(request, ("You buyed " + str(quantity) + " ticket.\nYou spend " + str(event.price*quantity) + "$"))

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
def ticket_preview(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    context = {"ticket": ticket}
    return render(request, 'ticket/ticket_review.html', context)


@login_required
def my_profile_view(request):
    user = request.user
    user_infos = UserProfile.objects.all().filter(user=user)
    context = {"user_infos": user_infos}
    return render(request, 'profile/profile.html', context)


@login_required
def edit_my_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/account/profile')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'profile/edit_profile.html', args)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/account/profile')
        else:
            return redirect('/account/change-password/')
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'profile/change_password.html', args)


@login_required
def add_event(request):
    if request.method == 'POST':
        form = AddEvent(request.POST or None)
        print(form.errors)
        if form.is_valid():
            event = form.save()
    return render(request, 'event/add_event.html', {'form': AddEvent})


@staff_member_required
def add_operator(request):
    form = ExtendedUserCreationForm(request.POST or None)
    profile_form = UserReg(request.POST or None)
    print(form.errors)
    if form.is_valid() and profile_form.is_valid():
        user = form.save()
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.isOperator = True
        profile.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'registration/signup.html',
                      {'form': ExtendedUserCreationForm, 'profile_form': UserReg})


@staff_member_required
def operators_list_view(request):
    operators_list = UserProfile.objects.all().filter(isOperator=True)
    context = {'operators_list': operators_list}
    return render(request, 'admin/operator_list_view.html', context)


@staff_member_required
def users_list_view(request):
    users_list = UserProfile.objects.all()
    context = {'users_list': users_list}
    return render(request, 'admin/user_list_view.html', context)


@staff_member_required
def list_all_events(request):
    accepted_event_list = Event.objects.all().filter(isAccepted=True, isAvailable=True)
    waiting_event_list = Event.objects.all().filter(isAccepted=False)
    disactive_event_list = Event.objects.all().filter(isAvailable=False)
    # bitmedi devam edicek
    context = {'accepted_event_list': accepted_event_list,
               'waiting_event_list': waiting_event_list,
               'disactive_event_list': disactive_event_list}


def add_balance(request):
    form = PaymentForm(request.POST or None)
    user = request.user
    user_infos = UserProfile.objects.get(user=user)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        user_infos.balance += amount
        user_infos.save()
        return redirect('my_profile')
    else:
        return render(request,'profile/add_balance.html',{'form':form})

