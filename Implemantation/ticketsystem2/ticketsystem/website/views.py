import datetime

from django.contrib import auth
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
import time
from django.contrib import messages
from .forms import EditEventForm, AddStage

from website.models import Event, Ticket, UserProfile, Stage
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


def go(request):
    redirect(request, 'home.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            auth.login(request, user)
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
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        birthday = request.POST['birthday']
        created_at = datetime.datetime.now()
        phone_number = request.POST['phone_number']
        converted = datetime.datetime.strptime(birthday, '%Y-%m-%d')
        gender = request.POST['gender']
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')
        if len(password1) < 8:
            messages.error(request, 'password does not less than 8 characters')
            return redirect('signup')
        if converted.year > created_at.year:
            messages.error(request, 'Invalid birthday date')
            return redirect('signup')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            messages.error(request, 'Email is already exist in the system.')
            return redirect('signup')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already exist in the system. Please enter a different username')
            return redirect('signup')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password1)
        profile = UserProfile(gender=gender, birthday=birthday, phone_number=phone_number, user=user)
        profile.save()
        user = authenticate(request, username=username, password=password1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username or password not correct')
            return redirect('signup')
    else:
        return render(request, 'registration/signup.html')


def event_preview(request, pk):
    event = get_object_or_404(Event, pk=pk)
    context = {"event": event}
    return render(request, 'event/event_review.html', context)


def search_event(request):
    return render(request, 'event/searchPage.html')


def event_check(request, event_id):
    event = Event.objects.get(pk=event_id)
    if event.isRejected:
        messages.error(request, 'Your request is rejected.')
    elif event.isAccepted:
        messages.success(request, 'Your request is accepted.')
    else:
        messages.error(request, 'Your request in queue.')
    return redirect('my_events')


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
                messages.error(request, ("No quota available for buying " + str(quantity) + " ticket"))
            elif user_infos.balance < event.price * quantity:
                messages.error(request, (
                        "Your amount is not enough for buying " + str(quantity) + " ticket.\nYou need " + str(
                    event.price * quantity - user_infos.balance) + "$ more."))

            else:
                user_infos.balance = user_infos.balance - event.price * quantity
                user_infos.save()
                event.quota -= quantity
                event.save()
                for i in range(0, int(quantity)):
                    ticket = Ticket(event=event, user=user)
                    ticket.save()

                messages.success(request, (
                        "You bought " + str(quantity) + " ticket.\nYou spend " + str(event.price * quantity) + "$"))

    else:
        form = BuyTicketForm()

    context = {'event': event, 'form': form}
    return render(request, 'ticket/buyTicketPage.html', context)


@login_required
def my_tickets_view(request):
    user = request.user
    user_infos = UserProfile.objects.all().filter(user=user)
    ticket_list = Ticket.objects.all().filter(user=user)
    context = {"ticket_list": ticket_list,
               "user_infos": user_infos}
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
    user = request.user
    user_info = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        user_info.gender = request.POST['gender']
        user_info.phone_number = request.POST['phone_number']
        user_info.birthday = request.POST['birthday']
        user_info.save()
        return redirect('my_profile')

    context = {"user_info": user_info}
    return render(request, 'profile/edit_profile.html', context)


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
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = AddEvent(request.POST or None)
        print(form.errors)
        if form.is_valid():
            event = form.save()
            event.owner = user_profile
            event.save()
            return redirect('my_events')
        else:
            return redirect('add_event')
    return render(request, 'event/add_event.html', {'form': AddEvent})


@login_required
def my_events(request):
    user_profile = UserProfile.objects.get(user=request.user)
    event_list = Event.objects.all().filter(owner=user_profile)
    context = {'event_list': event_list}
    return render(request, 'event/my_events.html', context)


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
def waiting_events(request):
    waiting_event_list = Event.objects.all().filter(isAccepted=False, isRejected=False)
    context = {'waiting_event_list': waiting_event_list}
    return render(request, 'admin/waiting_events_view.html', context)


@staff_member_required
def rejected_events(request):
    rejected_event_list = Event.objects.all().filter(isRejected=True)
    context = {'rejected_event_list': rejected_event_list}
    return render(request, 'admin/rejected_events_view.html', context)


@staff_member_required
def accepted_events(request):
    accepted_event_list = Event.objects.all().filter(isAccepted=True, isAvailable=True)
    context = {'accepted_event_list': accepted_event_list}
    return render(request, 'admin/accepted_events_view.html', context)


@staff_member_required
def disactive_events(request):
    disactive_event_list = Event.objects.all().filter(isAvailable=False)
    context = {'disactive_event_list': disactive_event_list}
    return render(request, 'admin/disactive_events_view.html', context)


@staff_member_required
def approve_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.isAccepted = True
    event.isAvailable = True
    event.save()
    return redirect('active_events')


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
        return render(request, 'profile/add_balance.html', {'form': form})


def edit_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    user = request.user
    user_infos = UserProfile.objects.get(user=user)
    if request.method == 'POST':

        form = EditEventForm(request.POST, instance=event)

        if form.is_valid():
            form.save()
            return redirect('/account/profile')
    else:

        form = EditEventForm(instance=event)
        args = {'form': form,
                'user_infos': user_infos}
        return render(request, 'event/edit_event.html', args)


def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    ticket_list = Ticket.objects.all().filter(event=event)
    for ticket in ticket_list:
        user_profile = UserProfile.objects.get(user=ticket.user)
        user_profile.balance += event.price
        user_profile.save()
    event.delete()
    return redirect('my_events')


def type_event_get(request, type):
    event_list = Event.objects.all().filter(type=type)
    return event_list


def concert_events(request):
    return render(request, 'ticket/concert-events.html', {'concert_list': type_event_get(request, 'C')})


def theatre_events(request):
    return render(request, 'ticket/theatre-events.html', {'theatre_list': type_event_get(request, 'T')})


def sport_events(request):
    return render(request, 'ticket/sport-events.html', {'sport_list': type_event_get(request, 'S')})


def reject_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.isRejected = True
    event.save()
    return redirect('waiting_events')


def add_stage_view(request):
    form = AddStage(request.POST or None)
    if request.method == 'POST':
        form = AddStage(request.POST or None)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('stage_all')
        else:
            return redirect('stage_add')
    return render(request, 'admin/add_stage.html', {'form': form})


def stage_list_view(request):
    stage_list = Stage.objects.all().filter()
    context = {'stage_list': stage_list}
    return render(request, 'admin/stage_list_view.html', context)


def edit_stage_view(request, stage_id):
    stage = Stage.objects.get(pk=stage_id)
    if request.method == 'POST':

        form = AddStage(request.POST, instance=stage)

        if form.is_valid():
            form.save()
            return redirect('stage_all')
    else:

        form = AddStage(instance=stage)
        args = {'form': form}
        return render(request, 'admin/add_stage.html', args)


def delete_stage_view(request, stage_id):
    stage = Stage.objects.get(pk=stage_id)
    event_list = Event.objects.all().filter(stage=stage)
    if len(event_list) > 0:
        stage.delete()
    else:
        messages.error(request, "You cannot delete this stage. There will be an event on this stage.")
    return redirect('stage_all')
